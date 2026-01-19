"""
Platform-specific scrapers for various e-commerce platforms.
"""

from .amazon_scraper import AmazonScraper
from .ebay_scraper import EbayScraper
from .shopify_scraper import ShopifyScraper
from .generic_scraper import GenericScraper

__all__ = ["AmazonScraper", "EbayScraper", "ShopifyScraper", "GenericScraper"]
