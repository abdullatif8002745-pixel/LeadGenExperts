"""
Main E-commerce Scraper
Auto-detects platform and uses appropriate scraper.
"""

from typing import Dict, List, Optional
from urllib.parse import urlparse
import logging

from .platforms.amazon_scraper import AmazonScraper
from .platforms.ebay_scraper import EbayScraper
from .platforms.shopify_scraper import ShopifyScraper
from .platforms.generic_scraper import GenericScraper

logging.basicConfig(level=logging.INFO)


class EcommerceScraper:
    """Main scraper class that auto-detects platform and delegates to appropriate scraper."""

    PLATFORM_SCRAPERS = {
        'amazon': AmazonScraper,
        'ebay': EbayScraper,
        'shopify': ShopifyScraper,
    }

    def __init__(self, rate_limit: float = 2.0, use_selenium: bool = False):
        """
        Initialize the e-commerce scraper.

        Args:
            rate_limit: Minimum seconds between requests
            use_selenium: Whether to use Selenium for dynamic content
        """
        self.rate_limit = rate_limit
        self.use_selenium = use_selenium
        self.logger = logging.getLogger(__name__)
        self._scrapers = {}

    def detect_platform(self, url: str) -> str:
        """
        Detect e-commerce platform from URL.

        Args:
            url: Product or store URL

        Returns:
            Platform name ('amazon', 'ebay', 'shopify', 'generic')
        """
        domain = urlparse(url).netloc.lower()

        if 'amazon.' in domain:
            return 'amazon'
        elif 'ebay.' in domain:
            return 'ebay'
        elif 'shopify.com' in domain or 'myshopify.com' in domain:
            return 'shopify'
        else:
            return 'generic'

    def get_scraper(self, platform: str):
        """Get or create a scraper instance for the platform."""
        if platform not in self._scrapers:
            scraper_class = self.PLATFORM_SCRAPERS.get(platform, GenericScraper)
            self._scrapers[platform] = scraper_class(
                rate_limit=self.rate_limit,
                use_selenium=self.use_selenium
            )
        return self._scrapers[platform]

    def scrape_product(self, url: str, platform: Optional[str] = None) -> Dict:
        """
        Scrape a single product from any e-commerce platform.

        Args:
            url: Product URL
            platform: Optional platform override (auto-detected if not provided)

        Returns:
            Dictionary containing product information
        """
        if platform is None:
            platform = self.detect_platform(url)

        self.logger.info(f"Detected platform: {platform}")
        scraper = self.get_scraper(platform)

        return scraper.scrape_product(url)

    def scrape_products(self, urls: List[str]) -> List[Dict]:
        """
        Scrape multiple products from various platforms.

        Args:
            urls: List of product URLs

        Returns:
            List of product dictionaries
        """
        products = []
        total = len(urls)

        for idx, url in enumerate(urls, 1):
            self.logger.info(f"Scraping product {idx}/{total}")
            try:
                product = self.scrape_product(url)
                if product:
                    products.append(product)
            except Exception as e:
                self.logger.error(f"Error scraping {url}: {e}")

        return products

    def scrape_category(self, url: str, max_products: int = 50, platform: Optional[str] = None) -> List[Dict]:
        """
        Scrape multiple products from a category page.

        Args:
            url: Category/listing page URL
            max_products: Maximum number of products to scrape
            platform: Optional platform override

        Returns:
            List of product dictionaries
        """
        if platform is None:
            platform = self.detect_platform(url)

        scraper = self.get_scraper(platform)

        if hasattr(scraper, 'scrape_category'):
            return scraper.scrape_category(url, max_products)
        else:
            self.logger.warning(f"Category scraping not implemented for {platform}")
            return []
