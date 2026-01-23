import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

class WebsiteScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def get_page_content(self, url, timeout=10):
        """Fetch page content with error handling"""
        try:
            response = self.session.get(url, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None

    def find_contact_pages(self, soup, base_url):
        """Find contact, about, and footer pages"""
        contact_urls = set()
        contact_keywords = ['contact', 'about', 'about-us', 'reach-us', 'get-in-touch', 'location']

        # Find links that might lead to contact pages
        for link in soup.find_all('a', href=True):
            href = link.get('href', '').lower()
            text = link.get_text().lower()

            if any(keyword in href or keyword in text for keyword in contact_keywords):
                full_url = urljoin(base_url, link['href'])
                if self.domain in urlparse(full_url).netloc:
                    contact_urls.add(full_url)

        return list(contact_urls)[:3]  # Limit to 3 contact pages

    def extract_company_name(self, soup):
        """Extract company name from various sources"""
        # Try meta tags first
        og_site_name = soup.find('meta', property='og:site_name')
        if og_site_name and og_site_name.get('content'):
            return og_site_name['content'].strip()

        # Try title tag
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text().strip()
            # Remove common suffixes
            title = re.sub(r'\s*[\|\-–—]\s*.*$', '', title)
            if title and len(title) < 100:
                return title

        # Try logo alt text or heading
        logo = soup.find('img', class_=re.compile(r'logo', re.I))
        if logo and logo.get('alt'):
            return logo['alt'].strip()

        # Try h1 or prominent headings
        h1 = soup.find('h1')
        if h1 and len(h1.get_text().strip()) < 50:
            return h1.get_text().strip()

        # Try navigation brand/logo text
        nav_brand = soup.find(class_=re.compile(r'brand|logo|site-name', re.I))
        if nav_brand:
            return nav_brand.get_text().strip()

        return "Not Found"

    def extract_phone_numbers(self, text):
        """Extract phone numbers from text"""
        # Various phone number patterns
        patterns = [
            r'\+?1?\s*\(?(\d{3})\)?[\s.-]*(\d{3})[\s.-]*(\d{4})',
            r'\+?\d{1,3}[\s.-]?\(?\d{2,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{3,4}',
            r'tel:\s*\+?[\d\s\-\(\)]+',
        ]

        phones = set()
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    phone = ''.join(match)
                else:
                    phone = match.replace('tel:', '').strip()

                # Clean and validate
                phone = re.sub(r'[^\d+]', '', phone)
                if len(phone) >= 10:
                    phones.add(phone)

        return list(phones)

    def extract_emails(self, text):
        """Extract email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)

        # Filter out common false positives
        filtered_emails = [
            email for email in emails
            if not any(x in email.lower() for x in ['example.com', 'domain.com', 'test.com', 'wixpress.com', 'sentry.io'])
        ]

        return list(set(filtered_emails))

    def extract_address(self, soup):
        """Extract physical address from page"""
        addresses = []

        # Look for address in schema.org markup
        address_schema = soup.find(attrs={'itemtype': re.compile(r'schema.org/PostalAddress', re.I)})
        if address_schema:
            address_parts = []
            for prop in ['streetAddress', 'addressLocality', 'addressRegion', 'postalCode']:
                elem = address_schema.find(attrs={'itemprop': prop})
                if elem:
                    address_parts.append(elem.get_text().strip())
            if address_parts:
                addresses.append(', '.join(address_parts))

        # Look in footer or address tags
        for tag in soup.find_all(['address', 'div', 'p'], class_=re.compile(r'address|location|contact', re.I)):
            text = tag.get_text().strip()
            # Simple heuristic: contains street/city patterns
            if re.search(r'\d+\s+\w+\s+(street|st|avenue|ave|road|rd|boulevard|blvd|drive|dr)', text, re.I):
                addresses.append(text)

        # Look for specific address patterns in text
        address_pattern = r'\d+\s+[\w\s]+(?:street|st|avenue|ave|road|rd|boulevard|blvd|drive|dr|lane|ln)[\w\s,]+\d{5}'
        matches = re.findall(address_pattern, soup.get_text(), re.I)
        addresses.extend(matches)

        return addresses[0] if addresses else "Not Found"

    def extract_social_links(self, soup):
        """Extract all social media links"""
        social_platforms = {
            'facebook.com': 'Facebook',
            'twitter.com': 'Twitter',
            'x.com': 'Twitter/X',
            'linkedin.com': 'LinkedIn',
            'instagram.com': 'Instagram',
            'youtube.com': 'YouTube',
            'pinterest.com': 'Pinterest',
            'tiktok.com': 'TikTok',
            'github.com': 'GitHub',
            'medium.com': 'Medium',
            'reddit.com': 'Reddit',
            'whatsapp.com': 'WhatsApp',
            'telegram.org': 'Telegram',
            't.me': 'Telegram'
        }

        social_links = {}

        for link in soup.find_all('a', href=True):
            href = link['href'].lower()
            for platform_domain, platform_name in social_platforms.items():
                if platform_domain in href:
                    # Clean the URL
                    full_url = urljoin(self.base_url, link['href'])
                    if platform_name not in social_links:
                        social_links[platform_name] = full_url

        return social_links

    def scrape_website(self):
        """Main scraping method"""
        print(f"Starting to scrape: {self.base_url}")

        # Initialize results
        results = {
            'company_name': 'Not Found',
            'phone': 'Not Found',
            'email': 'Not Found',
            'address': 'Not Found',
            'social_links': {},
            'url': self.base_url
        }

        # Get main page
        main_content = self.get_page_content(self.base_url)
        if not main_content:
            return results

        main_soup = BeautifulSoup(main_content, 'lxml')

        # Extract company name from main page
        results['company_name'] = self.extract_company_name(main_soup)

        # Extract social links from main page
        results['social_links'] = self.extract_social_links(main_soup)

        # Find contact pages
        contact_pages = self.find_contact_pages(main_soup, self.base_url)

        # Add main page to search list
        pages_to_search = [self.base_url] + contact_pages

        all_text = ""
        all_soups = [main_soup]

        # Scrape contact pages
        for page_url in contact_pages[:2]:  # Limit to 2 additional pages
            time.sleep(0.5)  # Be polite
            content = self.get_page_content(page_url)
            if content:
                soup = BeautifulSoup(content, 'lxml')
                all_soups.append(soup)
                all_text += " " + soup.get_text()

        # Extract contact information from all pages
        # Priority: footer and contact sections
        for soup in all_soups:
            # Check footer first
            footer = soup.find('footer')
            if footer:
                footer_text = footer.get_text()

                # Extract phone from footer
                if results['phone'] == 'Not Found':
                    phones = self.extract_phone_numbers(footer_text)
                    if phones:
                        results['phone'] = phones[0]

                # Extract email from footer
                if results['email'] == 'Not Found':
                    emails = self.extract_emails(footer_text)
                    if emails:
                        results['email'] = emails[0]

                # Extract address from footer
                if results['address'] == 'Not Found':
                    address = self.extract_address(footer)
                    if address != 'Not Found':
                        results['address'] = address

            # Check contact sections
            contact_sections = soup.find_all(['div', 'section'], class_=re.compile(r'contact|footer', re.I))
            for section in contact_sections:
                section_text = section.get_text()

                if results['phone'] == 'Not Found':
                    phones = self.extract_phone_numbers(section_text)
                    if phones:
                        results['phone'] = phones[0]

                if results['email'] == 'Not Found':
                    emails = self.extract_emails(section_text)
                    if emails:
                        results['email'] = emails[0]

        # If still not found, search entire page
        full_text = main_soup.get_text() + all_text

        if results['phone'] == 'Not Found':
            phones = self.extract_phone_numbers(full_text)
            if phones:
                results['phone'] = phones[0]

        if results['email'] == 'Not Found':
            emails = self.extract_emails(full_text)
            if emails:
                results['email'] = emails[0]

        if results['address'] == 'Not Found':
            for soup in all_soups:
                address = self.extract_address(soup)
                if address != 'Not Found':
                    results['address'] = address
                    break

        # Format social links as string
        if results['social_links']:
            social_str = ', '.join([f"{name}: {url}" for name, url in results['social_links'].items()])
            results['social_links'] = social_str
        else:
            results['social_links'] = 'Not Found'

        print(f"Scraping completed for: {self.base_url}")
        return results


def scrape_url(url):
    """Helper function to scrape a URL"""
    # Ensure URL has protocol
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    scraper = WebsiteScraper(url)
    return scraper.scrape_website()
