"""
Amazon Product Scraper
Specialized scraper for Amazon.com and international Amazon sites.
"""

from typing import Dict, List, Optional
from ..base_scraper import BaseScraper


class AmazonScraper(BaseScraper):
    """Scraper for Amazon product pages."""

    def scrape_product(self, url: str) -> Dict:
        """
        Scrape Amazon product information.

        Args:
            url: Amazon product URL

        Returns:
            Dictionary with product details
        """
        html = self.fetch_page(url)
        if not html:
            return {}

        soup = self.parse_html(html)

        product = {
            'url': url,
            'platform': 'amazon',
            'title': self._extract_title(soup),
            'price': self._extract_price(soup),
            'currency': self._extract_currency(soup),
            'availability': self._extract_availability(soup),
            'rating': self._extract_rating(soup),
            'review_count': self._extract_review_count(soup),
            'images': self._extract_images(soup),
            'description': self._extract_description(soup),
            'features': self._extract_features(soup),
            'specifications': self._extract_specifications(soup),
            'brand': self._extract_brand(soup),
            'category': self._extract_category(soup),
            'asin': self._extract_asin(url, soup)
        }

        return product

    def _extract_title(self, soup) -> str:
        """Extract product title."""
        selectors = [
            '#productTitle',
            'h1.a-size-large',
            'h1#title'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return self.clean_text(element.get_text())
        return ""

    def _extract_price(self, soup) -> Optional[float]:
        """Extract product price."""
        selectors = [
            '.a-price .a-offscreen',
            '#priceblock_ourprice',
            '#priceblock_dealprice',
            '.a-price-whole',
            'span.a-price span.a-offscreen'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text()
                return self.extract_price(price_text)
        return None

    def _extract_currency(self, soup) -> str:
        """Extract currency symbol."""
        price_element = soup.select_one('.a-price-symbol')
        if price_element:
            return self.clean_text(price_element.get_text())

        price_text = soup.select_one('.a-price .a-offscreen')
        if price_text:
            text = price_text.get_text()
            if '$' in text:
                return 'USD'
            elif '£' in text:
                return 'GBP'
            elif '€' in text:
                return 'EUR'
        return 'USD'

    def _extract_availability(self, soup) -> str:
        """Extract availability status."""
        selectors = [
            '#availability span',
            '.a-size-medium.a-color-success',
            '.a-size-medium.a-color-price'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return self.clean_text(element.get_text())
        return "Unknown"

    def _extract_rating(self, soup) -> Optional[float]:
        """Extract product rating."""
        rating_element = soup.select_one('span.a-icon-alt')
        if rating_element:
            rating_text = rating_element.get_text()
            try:
                return float(rating_text.split()[0])
            except (ValueError, IndexError):
                pass

        rating_element = soup.select_one('[data-hook="rating-out-of-text"]')
        if rating_element:
            rating_text = rating_element.get_text()
            try:
                return float(rating_text.split()[0])
            except (ValueError, IndexError):
                pass

        return None

    def _extract_review_count(self, soup) -> int:
        """Extract number of reviews."""
        selectors = [
            '#acrCustomerReviewText',
            '[data-hook="total-review-count"]'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text().replace(',', '')
                import re
                match = re.search(r'\d+', text)
                if match:
                    return int(match.group())
        return 0

    def _extract_images(self, soup) -> List[str]:
        """Extract product images."""
        images = []

        img_elements = soup.select('#altImages img')
        for img in img_elements:
            src = img.get('src', '')
            if src and 'https://' in src:
                large_src = src.replace('_SS40_', '_SL1500_')
                images.append(large_src)

        main_image = soup.select_one('#landingImage')
        if main_image and main_image.get('src'):
            images.insert(0, main_image['src'])

        return list(dict.fromkeys(images))[:10]

    def _extract_description(self, soup) -> str:
        """Extract product description."""
        desc_element = soup.select_one('#productDescription p')
        if desc_element:
            return self.clean_text(desc_element.get_text())

        desc_element = soup.select_one('#feature-bullets')
        if desc_element:
            return self.clean_text(desc_element.get_text())

        return ""

    def _extract_features(self, soup) -> List[str]:
        """Extract bullet point features."""
        features = []
        feature_elements = soup.select('#feature-bullets li span.a-list-item')

        for element in feature_elements:
            text = self.clean_text(element.get_text())
            if text and len(text) > 5:
                features.append(text)

        return features

    def _extract_specifications(self, soup) -> Dict[str, str]:
        """Extract technical specifications."""
        specs = {}

        spec_table = soup.select('#productDetails_techSpec_section_1 tr')
        for row in spec_table:
            cells = row.find_all('td')
            if len(cells) == 2:
                key = self.clean_text(cells[0].get_text())
                value = self.clean_text(cells[1].get_text())
                specs[key] = value

        detail_bullets = soup.select('#detailBullets_feature_div li')
        for item in detail_bullets:
            text = item.get_text()
            if ':' in text:
                parts = text.split(':', 1)
                key = self.clean_text(parts[0])
                value = self.clean_text(parts[1])
                specs[key] = value

        return specs

    def _extract_brand(self, soup) -> str:
        """Extract brand name."""
        brand_element = soup.select_one('#bylineInfo')
        if brand_element:
            text = brand_element.get_text()
            return self.clean_text(text.replace('Visit the', '').replace('Store', '').replace('Brand:', ''))

        brand_element = soup.select_one('a#brand')
        if brand_element:
            return self.clean_text(brand_element.get_text())

        return ""

    def _extract_category(self, soup) -> List[str]:
        """Extract product category breadcrumb."""
        categories = []
        breadcrumb = soup.select('#wayfinding-breadcrumbs_container li a')

        for link in breadcrumb:
            category = self.clean_text(link.get_text())
            if category:
                categories.append(category)

        return categories

    def _extract_asin(self, url: str, soup) -> str:
        """Extract ASIN (Amazon Standard Identification Number)."""
        import re

        asin_match = re.search(r'/dp/([A-Z0-9]{10})', url)
        if asin_match:
            return asin_match.group(1)

        asin_match = re.search(r'/gp/product/([A-Z0-9]{10})', url)
        if asin_match:
            return asin_match.group(1)

        detail_bullets = soup.select('#detailBullets_feature_div li')
        for item in detail_bullets:
            text = item.get_text()
            if 'ASIN' in text:
                asin_match = re.search(r'[A-Z0-9]{10}', text)
                if asin_match:
                    return asin_match.group(0)

        return ""
