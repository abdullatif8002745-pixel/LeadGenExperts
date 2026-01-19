#!/usr/bin/env python3
"""
E-commerce Web Scraper - Main CLI Interface
Command-line tool for scraping product information from e-commerce websites.
"""

import argparse
import sys
from typing import List
from scraper import EcommerceScraper
from scraper.exporters import DataExporter


def scrape_single_url(url: str, output_format: str, output_dir: str, rate_limit: float):
    """Scrape a single product URL."""
    print(f"Scraping: {url}")

    scraper = EcommerceScraper(rate_limit=rate_limit)
    product = scraper.scrape_product(url)

    if not product:
        print("Failed to scrape product")
        return 1

    print(f"✓ Successfully scraped: {product.get('title', 'N/A')[:60]}")

    exporter = DataExporter(output_dir=output_dir)

    if output_format == 'json':
        filepath = exporter.export_json([product])
    elif output_format == 'csv':
        filepath = exporter.export_csv([product])
    elif output_format == 'excel':
        filepath = exporter.export_excel([product])
    elif output_format == 'all':
        files = exporter.export_all([product])
        print("\nExported to:")
        for fmt, path in files.items():
            print(f"  {fmt.upper()}: {path}")
        return 0

    print(f"Exported to: {filepath}")
    return 0


def scrape_multiple_urls(urls: List[str], output_format: str, output_dir: str, rate_limit: float):
    """Scrape multiple product URLs."""
    print(f"Scraping {len(urls)} products...")

    scraper = EcommerceScraper(rate_limit=rate_limit)
    products = scraper.scrape_products(urls)

    if not products:
        print("No products were successfully scraped")
        return 1

    print(f"\n✓ Successfully scraped {len(products)}/{len(urls)} products")

    exporter = DataExporter(output_dir=output_dir)

    if output_format == 'json':
        filepath = exporter.export_json(products)
    elif output_format == 'csv':
        filepath = exporter.export_csv(products)
    elif output_format == 'excel':
        filepath = exporter.export_excel(products)
    elif output_format == 'all':
        files = exporter.export_all(products)
        print("\nExported to:")
        for fmt, path in files.items():
            print(f"  {fmt.upper()}: {path}")
        return 0

    print(f"Exported to: {filepath}")
    return 0


def scrape_from_file(filepath: str, output_format: str, output_dir: str, rate_limit: float):
    """Scrape URLs from a text file (one URL per line)."""
    try:
        with open(filepath, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]

        if not urls:
            print(f"No URLs found in {filepath}")
            return 1

        return scrape_multiple_urls(urls, output_format, output_dir, rate_limit)

    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return 1
    except Exception as e:
        print(f"Error reading file: {e}")
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="E-commerce Web Scraper - Extract product information from online stores",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape a single product
  python main.py --url "https://www.amazon.com/dp/B08N5WRWNW"

  # Scrape multiple products and export to CSV
  python main.py --urls "url1" "url2" "url3" --format csv

  # Scrape URLs from a file
  python main.py --file urls.txt --format excel

  # Export to all formats
  python main.py --url "https://example.com/product" --format all

  # Custom output directory and rate limit
  python main.py --url "https://example.com/product" --output data --rate-limit 3.0
        """
    )

    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--url',
        type=str,
        help='Single product URL to scrape'
    )
    input_group.add_argument(
        '--urls',
        nargs='+',
        help='Multiple product URLs to scrape'
    )
    input_group.add_argument(
        '--file',
        type=str,
        help='Text file containing URLs (one per line)'
    )

    # Output options
    parser.add_argument(
        '--format',
        choices=['json', 'csv', 'excel', 'all'],
        default='json',
        help='Output format (default: json)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='output',
        help='Output directory (default: output)'
    )

    # Scraping options
    parser.add_argument(
        '--rate-limit',
        type=float,
        default=2.0,
        help='Minimum seconds between requests (default: 2.0)'
    )
    parser.add_argument(
        '--selenium',
        action='store_true',
        help='Use Selenium for dynamic content (requires setup)'
    )

    args = parser.parse_args()

    # Display configuration
    print("=" * 70)
    print("E-COMMERCE WEB SCRAPER")
    print("=" * 70)
    print(f"Output format: {args.format}")
    print(f"Output directory: {args.output}")
    print(f"Rate limit: {args.rate_limit}s")
    print("=" * 70)
    print()

    # Execute scraping
    if args.url:
        return scrape_single_url(args.url, args.format, args.output, args.rate_limit)
    elif args.urls:
        return scrape_multiple_urls(args.urls, args.format, args.output, args.rate_limit)
    elif args.file:
        return scrape_from_file(args.file, args.format, args.output, args.rate_limit)


if __name__ == "__main__":
    sys.exit(main())
