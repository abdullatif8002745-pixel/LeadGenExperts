#!/usr/bin/env python3
"""
awards_extractor.py
===================
Extract film award nominees and winners from Wikipedia ceremony pages.

Supported ceremonies (auto-detected from URL):
  • BAFTA   — e.g. https://en.wikipedia.org/wiki/78th_British_Academy_Film_Awards
  • Oscars  — e.g. https://en.wikipedia.org/wiki/96th_Academy_Awards
  • Cannes  — e.g. https://en.wikipedia.org/wiki/2023_Cannes_Film_Festival

Output schema:
  Year | Category | Title | Type | Person | Won | Multiple Names

Usage (single year):
    python awards_extractor.py "https://en.wikipedia.org/wiki/78th_British_Academy_Film_Awards"

Usage (many years — write one URL per line in a text file):
    python awards_extractor.py --batch bafta_urls.txt --output bafta_all_years

Options:
    --output STEM   Base name for .csv / .xlsx output  (default: "awards")
    --no-verify     Skip the cross-check verification step
    --batch FILE    Text file with one Wikipedia URL per line (#-comments ok)
"""

import argparse
import csv
import json
import re
import sys
import time
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent
ALIASES_FILE = SCRIPT_DIR / "aliases.json"
HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; FilmAwardsResearch/1.0)"}
COLUMNS = ["Year", "Category", "Title", "Type", "Person", "Won", "Multiple Names"]

# Default alias table written on first run — edit aliases.json directly to extend.
DEFAULT_ALIASES: dict = {
    "_comment": "Map non-canonical spellings → canonical. Keys are exact strings found on Wikipedia.",
    "titles": {
        "Zootropolis": "Zootopia",
        "Zootropolis 2": "Zootopia 2",
        "The Favourite": "The Favorite",
        "Mr Burton": "Mr. Burton",
        "Emilia Perez": "Emilia Pérez",
    },
    "people": {
        "Chloe Zhao": "Chloé Zhao",
        "Pedro Almodovar": "Pedro Almodóvar",
        "Audrey Diwan": "Audrey Diwan",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# ALIAS / NORMALIZATION
# ─────────────────────────────────────────────────────────────────────────────

def load_aliases() -> dict:
    if ALIASES_FILE.exists():
        with open(ALIASES_FILE, encoding="utf-8") as fh:
            return json.load(fh)
    with open(ALIASES_FILE, "w", encoding="utf-8") as fh:
        json.dump(DEFAULT_ALIASES, fh, indent=2, ensure_ascii=False)
    print(f"[info] Created default aliases file: {ALIASES_FILE}")
    return DEFAULT_ALIASES


def normalize(text: str, aliases: dict, kind: str = "titles") -> str:
    """
    1. Strip whitespace.
    2. Unicode NFC-compose (handles decomposed vs. precomposed accents).
    3. Remove trailing Wikipedia disambiguation suffixes like "(film)", "(filmmaker)".
    4. Apply alias lookup (exact match only — edit aliases.json for fuzzy cases).
    """
    text = text.strip()
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"\s*\((film|filmmaker|producer|director)\)\s*$", "", text, flags=re.I)
    lookup = aliases.get(kind, {})
    return lookup.get(text, text)


# ─────────────────────────────────────────────────────────────────────────────
# HTTP FETCH
# ─────────────────────────────────────────────────────────────────────────────

def fetch_soup(url: str, retries: int = 4) -> BeautifulSoup:
    for attempt in range(retries):
        try:
            r = requests.get(url, headers=HTTP_HEADERS, timeout=30)
            r.raise_for_status()
            return BeautifulSoup(r.text, "lxml")
        except Exception as exc:
            if attempt < retries - 1:
                wait = 2 ** attempt
                print(f"  [warn] Fetch attempt {attempt+1} failed ({exc}); retrying in {wait}s…")
                time.sleep(wait)
            else:
                raise RuntimeError(f"Could not fetch {url}: {exc}") from exc


# ─────────────────────────────────────────────────────────────────────────────
# CEREMONY AUTO-DETECTION
# ─────────────────────────────────────────────────────────────────────────────

def detect_type(url: str) -> str:
    u = url.lower()
    if "british_academy" in u or "bafta" in u:
        return "bafta"
    if "academy_award" in u or "oscars" in u:
        return "oscars"
    if "cannes" in u:
        return "cannes"
    return "unknown"


def extract_year(soup: BeautifulSoup, url: str) -> str:
    """Read ceremony year from the infobox Date row; fall back to URL."""
    infobox = soup.find("table", class_="infobox")
    if infobox:
        for th in infobox.find_all("th"):
            if re.search(r"\bDate\b", th.get_text(), re.I):
                td = th.find_next_sibling("td")
                if td:
                    m = re.search(r"\b(19|20)\d{2}\b", td.get_text())
                    if m:
                        return m.group(0)
    m = re.search(r"\b(19|20)\d{2}\b", url)
    return m.group(0) if m else "Unknown"


# ─────────────────────────────────────────────────────────────────────────────
# BAFTA / OSCARS PARSER   (shared wikitable format)
# ─────────────────────────────────────────────────────────────────────────────
# Wikipedia structure for both ceremonies:
#
#   <table class="wikitable">
#     <tr>
#       <td>                              ← one td = one award category
#         <div><b>Category Name</b></div>
#         <ul>
#           <li>                          ← THE WINNER (only top-level li)
#             <b><i>Film</i> – Person…</b>
#             <ul>                        ← nominees nested inside winner li
#               <li><i>Film</i> – Person…</li>
#               …
#             </ul>
#           </li>
#         </ul>
#       </td>
#       <td>…</td>                        ← next category in the same row
#     </tr>
#   </table>

def _tag_direct_text(tag: Tag) -> str:
    """
    Concatenate text from a tag's direct content,
    skipping any nested <ul>/<ol> sub-lists (which contain other nominees).
    Normalises internal whitespace.
    """
    buf: list[str] = []
    for child in tag.children:
        if isinstance(child, NavigableString):
            buf.append(str(child))
        elif child.name in ("ul", "ol"):
            continue  # skip sub-nominee lists
        else:
            buf.append(child.get_text(""))
    raw = "".join(buf).strip()
    return re.sub(r"\s+", " ", raw)


def _parse_li(li: Tag, aliases: dict) -> tuple[str, str]:
    """
    Parse one nominee <li> → (film_title, semicolon-separated persons).

    Wikipedia format (either order):
      <i>Film Title</i> – Person A, Person B, and Person C
      Person A – <i>Film Title</i>
    """
    text = _tag_direct_text(li)

    # Film title lives in the <i> tag
    i_tag = li.find("i")
    title = normalize(i_tag.get_text(), aliases, "titles") if i_tag else ""

    # Strip Oscar-style credit labels and dagger markers
    # e.g. ", producers ‡"  ", producer"  "‡"  "†"
    text = re.sub(r",?\s*producers?\s*[‡†]?", "", text, flags=re.I)
    text = re.sub(r"\s*[‡†]\s*", "", text)
    # Strip Wikipedia footnote refs like [22]
    text = re.sub(r"\[\d+\]", "", text)
    # Strip screenplay source credit: "; based on the novel…"
    text = re.sub(r"[;,]?\s*based on\b.*$", "", text, flags=re.I)
    # Strip inline "Screenplay by" / "Story by" credit labels
    text = re.sub(r"\b(Screenplay|Story|Written)\s+by\s+", "", text, flags=re.I)

    # Persons = everything left after removing film title and dash separator
    remainder = text
    if title:
        remainder = remainder.replace(title, "")
    # Strip leading and trailing dash/en-dash/em-dash
    remainder = re.sub(r"^[\s–—\-]+", "", remainder)
    remainder = re.sub(r"[\s–—\-]+$", "", remainder)

    # Strip trailing role descriptions: "as Character Name" or "as Bob Dylan"
    remainder = re.sub(r"\bas\b.*$", "", remainder, flags=re.I)
    # Clean up any dangling separator left after role strip  (e.g. "Adrien Brody –")
    remainder = re.sub(r"[\s–—\-,]+$", "", remainder).strip()

    # Split on ", " and " and "
    remainder = re.sub(r"\band\b", ",", remainder, flags=re.I)
    raw_names = [p.strip() for p in remainder.split(",") if p.strip() and len(p.strip()) > 1]
    names = [normalize(n, aliases, "people") for n in raw_names]

    return title, "; ".join(n for n in names if n)


def _make_row(year: str, category: str, title: str, person: str,
              won: bool, multiple: bool) -> dict:
    return {
        "Year": year,
        "Category": category,
        "Title": title,
        "Type": "movie",
        "Person": person,
        "Won": "TRUE" if won else "FALSE",
        "Multiple Names": "TRUE" if multiple else "FALSE",
    }


def parse_bafta_oscars(soup: BeautifulSoup, year: str, aliases: dict) -> list[dict]:
    rows: list[dict] = []

    for table in soup.find_all("table", class_="wikitable"):
        # Skip summary tables: they have a <caption> or style="text-align:center"
        if table.find("caption"):
            continue
        if "text-align:center" in table.get("style", ""):
            continue

        for td in table.find_all("td"):
            # Identify the category name from the header <div>
            cat_div = td.find("div")
            if not cat_div:
                continue
            category = re.sub(r"\[\d+\]", "", cat_div.get_text(strip=True)).strip()
            if not category:
                continue

            ul = td.find("ul")
            if not ul:
                continue

            top_lis = ul.find_all("li", recursive=False)
            if not top_lis:
                continue

            # Layout A (standard BAFTA/Oscar):
            #   single top-level li = winner, with a nested <ul> of nominees
            # Layout B (fallback):
            #   multiple top-level lis, first one with a direct <b> child = winner
            if len(top_lis) == 1 and top_lis[0].find("ul"):
                winner_li = top_lis[0]
                t, p = _parse_li(winner_li, aliases)
                rows.append(_make_row(year, category, t, p, True, p.count(";") >= 1))

                sub_ul = winner_li.find("ul")
                if sub_ul:
                    for li in sub_ul.find_all("li", recursive=False):
                        t2, p2 = _parse_li(li, aliases)
                        rows.append(_make_row(year, category, t2, p2, False, p2.count(";") >= 1))
            else:
                for li in top_lis:
                    # Winner = li whose first direct element-child is <b>
                    is_winner = any(
                        c.name == "b"
                        for c in li.children
                        if hasattr(c, "name")
                    )
                    t, p = _parse_li(li, aliases)
                    rows.append(_make_row(year, category, t, p, is_winner, p.count(";") >= 1))

    return rows


# ─────────────────────────────────────────────────────────────────────────────
# CANNES PARSER
# ─────────────────────────────────────────────────────────────────────────────
# Cannes uses two data sources combined:
#
#   Source 1 — "Official awards" section: <ul> lists with lines like
#     "Palme d'Or: Anatomy of a Fall by Justine Triet"
#     → these become Won=TRUE rows
#
#   Source 2 — "In Competition" screening table (FFDEAD-highlighted rows):
#     columns: English Title | Original Title | Director(s) | Country
#     All non-winner competition films become Won=FALSE rows for "Palme d'Or".

def _cannes_parse_award_li(li: Tag, section: str, aliases: dict) -> Optional[dict]:
    """
    Parse one <li> from a Cannes Official awards list.

    Strategy: use the <i> tag (if present) to pin the film title, then treat
    all remaining link/text content as the person field.  Fall back to plain-
    text heuristics when no <i> tag is present.

    Line formats encountered:
      "Palme d'Or: <i>Film</i> by Director"     → title=Film, person=Director
      "Best Director: Director for <i>Film</i>"  → title=Film, person=Director
      "Honorary Palme d'Or: Person Name"          → title="", person=PersonName
    """
    # Use _tag_direct_text so nested <ul> (e.g. Special Mention sub-items) are ignored
    raw = _tag_direct_text(li)
    raw = re.sub(r"\[\s*\d+\s*\]", "", raw)   # strip footnotes [35] or [ 35 ]
    raw = re.sub(r"\s+", " ", raw).strip()
    if not raw:
        return None

    # Split "Award Name: rest" on the FIRST colon
    if ":" in raw:
        category, rest = raw.split(":", 1)
        category = category.strip()
        rest = rest.strip()
    else:
        category = section
        rest = raw

    # Prefer <i> tag as the canonical film-title indicator
    i_tag = li.find("i")
    if i_tag:
        title = normalize(i_tag.get_text(), aliases, "titles")
        # Everything except the title and its surrounding separators is the person
        person_text = rest.replace(title, "")
        person_text = re.sub(r"\s*(by|for)\s*", "", person_text, flags=re.I)
        person_text = re.sub(r"[,;]+\s*$", "", person_text.strip())
        # Split on comma/"and" but only if result looks like names
        person_text = re.sub(r"\band\b", ",", person_text, flags=re.I)
        _generic = {"cast", "crew", "cast and crew", "cast & crew", ""}
        names = [normalize(n.strip(), aliases, "people")
                 for n in person_text.split(",")
                 if n.strip() and len(n.strip()) > 1
                 and n.strip().lower() not in _generic]
        person = "; ".join(n for n in names if n)
    else:
        # No <i> tag — text-only heuristics
        title, person = "", ""
        if " by " in rest:
            parts = rest.rsplit(" by ", 1)
            title = normalize(parts[0].strip(), aliases, "titles")
            person = normalize(parts[1].strip(), aliases, "people")
        elif " for " in rest:
            idx = rest.index(" for ")
            person = normalize(rest[:idx].strip(), aliases, "people")
            title = normalize(rest[idx + 5:].strip(), aliases, "titles")
        else:
            # Honour/special — whole rest is either a person or a film
            title = normalize(rest, aliases, "titles")

    return _make_row("", category, title, person, True, person.count(";") >= 1)


def parse_cannes(soup: BeautifulSoup, year: str, aliases: dict) -> list[dict]:
    rows: list[dict] = []

    # ── Source 1: Official awards winners ────────────────────────────────────
    in_official = False
    current_subsection = "In Competition"

    for tag in soup.find_all(["h2", "h3", "h4", "ul", "dl"]):
        txt = tag.get_text(strip=True)

        if tag.name == "h2":
            if "official award" in txt.lower():
                in_official = True
            elif in_official:
                break  # exited official awards section
            continue

        if not in_official:
            continue

        if tag.name in ("h3", "h4"):
            current_subsection = txt
            continue

        if tag.name == "ul":
            for li in tag.find_all("li", recursive=False):
                row = _cannes_parse_award_li(li, current_subsection, aliases)
                if row:
                    row["Year"] = year
                    rows.append(row)

        if tag.name == "dl":
            # Some Cannes pages use <dt>Award:</dt><dd>Film by Director</dd>
            # Wrap each dt/dd pair in a temporary BeautifulSoup li-equivalent
            dts = tag.find_all("dt")
            dds = tag.find_all("dd")
            for dt, dd in zip(dts, dds):
                # Build a synthetic li-like tag by combining dt and dd
                raw_line = dt.get_text(" ", strip=True).rstrip(":") + ": " + dd.get_text(" ", strip=True)
                raw_line = re.sub(r"\[\s*\d+\s*\]", "", raw_line)
                raw_line = re.sub(r"\s+", " ", raw_line).strip()
                if not raw_line:
                    continue
                # Simple text-only parse for dl entries (no <i> tag context here)
                cat, rest = (raw_line.split(":", 1) if ":" in raw_line
                             else (current_subsection, raw_line))
                cat, rest = cat.strip(), rest.strip()
                title, person = "", ""
                if " by " in rest:
                    p = rest.rsplit(" by ", 1)
                    title = normalize(p[0].strip(), aliases, "titles")
                    person = normalize(p[1].strip(), aliases, "people")
                elif " for " in rest:
                    idx = rest.index(" for ")
                    person = normalize(rest[:idx].strip(), aliases, "people")
                    title = normalize(rest[idx + 5:].strip(), aliases, "titles")
                else:
                    title = normalize(rest, aliases, "titles")
                row = _make_row(year, cat, title, person, True, person.count(";") >= 1)
                rows.append(row)

    # ── Source 2: Nominees from In Competition screening table ────────────────
    winner_titles = {r["Title"] for r in rows if r["Won"] == "TRUE"}

    all_tables = soup.find_all("table", class_="wikitable")
    for table in all_tables:
        prev_h = table.find_previous(["h2", "h3"])
        if not prev_h or "in competition" not in prev_h.get_text().lower():
            continue
        # Confirm it's a screening table (has a Director column)
        col_headers = [th.get_text(strip=True).lower() for th in table.find_all("th")]
        if not any("director" in h for h in col_headers):
            continue

        for tr in table.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) < 3:
                continue
            en_title = tds[0].get_text(strip=True)
            en_title = re.sub(r"\s*\(QP\)\s*$", "", en_title, flags=re.I).strip()
            en_title = normalize(en_title, aliases, "titles")
            director = normalize(tds[2].get_text(strip=True), aliases, "people")

            is_ffdead = "FFDEAD" in str(tr)
            # If already captured as a winner from source 1, skip
            if en_title in winner_titles:
                continue

            rows.append(_make_row(
                year, "Palme d'Or", en_title, director,
                is_ffdead, director.count(";") >= 1
            ))

    return rows


# ─────────────────────────────────────────────────────────────────────────────
# VERIFICATION
# ─────────────────────────────────────────────────────────────────────────────

def verify_winners(rows: list[dict], soup: BeautifulSoup) -> list[str]:
    """
    Cross-check parsed data against secondary signals on the same page.

    Check 1 — Category integrity:
        Every category must have exactly one winner row.

    Check 2 — Multiple-awards consistency:
        Films listed in the page's "multiple awards" summary table must appear
        as winners in two or more parsed categories.

    Returns a list of warning strings (empty list = all clear).
    """
    warnings: list[str] = []

    # ── Check 1 ──────────────────────────────────────────────────────────────
    winners_per_cat: dict[str, list[str]] = defaultdict(list)
    all_categories: set[str] = set()

    for r in rows:
        cat = r["Category"]
        all_categories.add(cat)
        if r["Won"] == "TRUE":
            winners_per_cat[cat].append(r["Title"] or r["Person"])

    for cat in all_categories:
        if cat not in winners_per_cat:
            warnings.append(f"NO WINNER found for category: '{cat}'")
        elif len(winners_per_cat[cat]) > 1:
            # Honorary / Special Mention categories legitimately have multiple recipients
            if re.search(r"\b(honorary|honorar|special mention)\b", cat, re.I):
                continue
            titles = ", ".join(winners_per_cat[cat])
            warnings.append(f"MULTIPLE WINNERS in '{cat}': {titles}")

    # ── Check 2 ──────────────────────────────────────────────────────────────
    multi_award_films: set[str] = set()
    for table in soup.find_all("table", class_="wikitable"):
        cap = table.find("caption")
        if not cap:
            continue
        cap_txt = cap.get_text().lower()
        if "multiple award" not in cap_txt and "multiple wins" not in cap_txt:
            continue
        for tr in table.find_all("tr")[1:]:
            tds = tr.find_all("td")
            if not tds:
                continue
            film = re.sub(r"\s*\(film\)\s*$", "", tds[-1].get_text(strip=True), flags=re.I)
            multi_award_films.add(film)

    if multi_award_films:
        won_counts: dict[str, int] = defaultdict(int)
        for r in rows:
            if r["Won"] == "TRUE" and r["Title"]:
                won_counts[r["Title"]] += 1

        for film in multi_award_films:
            count = won_counts.get(film, 0)
            if count < 2:
                # Case-insensitive fallback
                fuzzy_count = max(
                    (c for t, c in won_counts.items() if t.lower() == film.lower()),
                    default=0,
                )
                if fuzzy_count < 2:
                    warnings.append(
                        f"MISMATCH: '{film}' in 'multiple awards' table "
                        f"but only {max(count, fuzzy_count)} win(s) parsed"
                    )

    return warnings


# ─────────────────────────────────────────────────────────────────────────────
# OUTPUT: CSV + XLSX
# ─────────────────────────────────────────────────────────────────────────────

def write_csv(rows: list[dict], path: Path) -> None:
    with open(path, "w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"  [output] CSV  → {path}")


def write_xlsx(rows: list[dict], path: Path) -> None:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Awards"

    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="1F4E79")   # dark blue
    winner_fill = PatternFill("solid", fgColor="E2EFDA")   # light green

    # Header row
    ws.append(COLUMNS)
    for cell in ws[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", wrap_text=False)

    # Data rows
    for row in rows:
        ws.append([row.get(c, "") for c in COLUMNS])
        if row.get("Won") == "TRUE":
            for cell in ws[ws.max_row]:
                cell.fill = winner_fill

    # Auto-size columns
    for col_idx, col_name in enumerate(COLUMNS, 1):
        col_letter = get_column_letter(col_idx)
        max_len = len(col_name)
        for row in rows:
            val = str(row.get(col_name, ""))
            if len(val) > max_len:
                max_len = len(val)
        ws.column_dimensions[col_letter].width = min(max_len + 3, 70)

    ws.freeze_panes = "A2"
    wb.save(path)
    print(f"  [output] XLSX → {path}")


# ─────────────────────────────────────────────────────────────────────────────
# ORCHESTRATION
# ─────────────────────────────────────────────────────────────────────────────

def process_url(url: str, aliases: dict, verify: bool = True) -> list[dict]:
    print(f"\n→ Fetching: {url}")
    soup = fetch_soup(url)

    ceremony_type = detect_type(url)
    year = extract_year(soup, url)
    print(f"  Ceremony type = {ceremony_type!r}   year = {year!r}")

    if ceremony_type in ("bafta", "oscars"):
        rows = parse_bafta_oscars(soup, year, aliases)
    elif ceremony_type == "cannes":
        rows = parse_cannes(soup, year, aliases)
    else:
        print("  [warn] Unknown ceremony type — attempting BAFTA/Oscars parser as fallback.")
        rows = parse_bafta_oscars(soup, year, aliases)

    winner_count = sum(1 for r in rows if r["Won"] == "TRUE")
    cat_count = len({r["Category"] for r in rows})
    print(f"  Extracted {len(rows)} rows across {cat_count} categories ({winner_count} winners)")

    if verify:
        warnings = verify_winners(rows, soup)
        if warnings:
            print(f"  [verify] {len(warnings)} warning(s):")
            for w in warnings:
                print(f"    ⚠  {w}")
        else:
            print("  [verify] ✓ No issues detected")

    return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("url", nargs="?", help="Wikipedia ceremony URL")
    src.add_argument(
        "--batch", metavar="FILE",
        help="Text file with one Wikipedia URL per line (# lines are comments)",
    )
    parser.add_argument(
        "--output", "-o", default="awards",
        help="Output file stem — creates <STEM>.csv and <STEM>.xlsx  (default: awards)",
    )
    parser.add_argument(
        "--no-verify", action="store_true",
        help="Skip the winner verification step",
    )
    args = parser.parse_args()

    aliases = load_aliases()

    if args.url:
        urls = [args.url]
    else:
        batch_path = Path(args.batch)
        if not batch_path.exists():
            sys.exit(f"[error] Batch file not found: {batch_path}")
        with open(batch_path, encoding="utf-8") as fh:
            urls = [
                line.strip()
                for line in fh
                if line.strip() and not line.startswith("#")
            ]

    all_rows: list[dict] = []
    for i, url in enumerate(urls):
        try:
            rows = process_url(url, aliases, verify=not args.no_verify)
            all_rows.extend(rows)
        except Exception as exc:
            print(f"  [error] Skipping {url}: {exc}")
        if i < len(urls) - 1:
            time.sleep(1)  # polite crawl delay

    if not all_rows:
        sys.exit("[error] No data extracted.")

    stem = Path(args.output)
    write_csv(all_rows, stem.with_suffix(".csv"))
    write_xlsx(all_rows, stem.with_suffix(".xlsx"))

    total_cats = len({r["Category"] for r in all_rows})
    print(
        f"\n✓ Done — {len(all_rows)} rows | "
        f"{total_cats} categories | "
        f"{len(urls)} URL(s)"
    )


if __name__ == "__main__":
    main()
