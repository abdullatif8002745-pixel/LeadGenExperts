"""
Base Scraper Class
Provides common functionality for all platform-specific scrapers.
"""

import time
import random
import requests
from typing import Dict, List, Optional
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class BaseScraper:
    """Base class for all e-commerce scrapers."""

    def __init__(self, rate_limit: float = 2.0, use_selenium: bool = False):
        """
        Initialize the base scraper.

        Args:
            rate_limit: Minimum seconds between requests (default: 2.0)
            use_selenium: Whether to use Selenium for dynamic content (default: False)
        """
        self.rate_limit = rate_limit
        self.use_selenium = use_selenium
        self.ua = UserAgent()
        self.session = requests.Session()
        self.last_request_time = 0
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_headers(self) -> Dict[str, str]:
        """Generate random headers to avoid blocking."""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def respect_rate_limit(self):
        """Ensure we respect rate limiting between requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            sleep_time = self.rate_limit - elapsed + random.uniform(0, 0.5)
            time.sleep(sleep_time)
        self.last_request_time = time.time()

    def fetch_page(self, url: str, max_retries: int = 3) -> Optional[str]:
        """
        Fetch a page with retry logic and error handling.

        Args:
            url: The URL to fetch
            max_retries: Maximum number of retry attempts

        Returns:
            HTML content as string, or None if failed
        """
        self.respect_rate_limit()

        for attempt in range(max_retries):
            try:
                response = self.session.get(
                    url,
                    headers=self.get_headers(),
                    timeout=10
                )
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                self.logger.warning(f"Attempt {attempt + 1}/{max_retries} failed for {url}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    self.logger.error(f"Failed to fetch {url} after {max_retries} attempts")
                    return None

    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content using BeautifulSoup."""
        return BeautifulSoup(html, 'lxml')

    def clean_text(self, text: Optional[str]) -> str:
        """Clean and normalize text data."""
        if not text:
            return ""
        return " ".join(text.strip().split())

    def extract_price(self, price_text: str) -> Optional[float]:
        """
        Extract numeric price from price text.

        Args:
            price_text: Raw price string (e.g., "$99.99", "£49.99")

        Returns:
            Float price or None if parsing failed
        """
        if not price_text:
            return None

        import re
        price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
        if price_match:
            try:
                return float(price_match.group())
            except ValueError:
                return None
        return None

    def scrape_product(self, url: str) -> Dict:
        """
        Scrape a single product. Should be implemented by subclasses.

        Args:
            url: Product URL

        Returns:
            Dictionary containing product information
        """
        raise NotImplementedError("Subclasses must implement scrape_product()")

    def scrape_products(self, urls: List[str]) -> List[Dict]:
        """
        Scrape multiple products.

        Args:
            urls: List of product URLs

        Returns:
            List of product dictionaries
        """
        products = []
        total = len(urls)

        for idx, url in enumerate(urls, 1):
            self.logger.info(f"Scraping product {idx}/{total}: {url}")
            try:
                product = self.scrape_product(url)
                if product:
                    products.append(product)
            except Exception as e:
                self.logger.error(f"Error scraping {url}: {e}")

        return products
