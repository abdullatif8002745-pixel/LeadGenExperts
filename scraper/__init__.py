"""
E-commerce Web Scraper
A comprehensive tool for scraping product information from various e-commerce platforms.
"""

from .ecommerce_scraper import EcommerceScraper
from .base_scraper import BaseScraper

__version__ = "1.0.0"
__all__ = ["EcommerceScraper", "BaseScraper"]
