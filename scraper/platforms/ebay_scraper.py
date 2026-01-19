"""
eBay Product Scraper
Specialized scraper for eBay listings.
"""

from typing import Dict, List, Optional
from ..base_scraper import BaseScraper


class EbayScraper(BaseScraper):
    """Scraper for eBay product listings."""

    def scrape_product(self, url: str) -> Dict:
        """
        Scrape eBay product information.

        Args:
            url: eBay product URL

        Returns:
            Dictionary with product details
        """
        html = self.fetch_page(url)
        if not html:
            return {}

        soup = self.parse_html(html)

        product = {
            'url': url,
            'platform': 'ebay',
            'title': self._extract_title(soup),
            'price': self._extract_price(soup),
            'currency': self._extract_currency(soup),
            'condition': self._extract_condition(soup),
            'availability': self._extract_availability(soup),
            'seller': self._extract_seller(soup),
            'seller_rating': self._extract_seller_rating(soup),
            'images': self._extract_images(soup),
            'description': self._extract_description(soup),
            'item_specifics': self._extract_item_specifics(soup),
            'shipping': self._extract_shipping(soup),
            'watchers': self._extract_watchers(soup),
            'sold_count': self._extract_sold_count(soup),
            'item_number': self._extract_item_number(soup)
        }

        return product

    def _extract_title(self, soup) -> str:
        """Extract product title."""
        selectors = [
            'h1.x-item-title__mainTitle',
            'h1[itemprop="name"]',
            '.it-ttl'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return self.clean_text(element.get_text())
        return ""

    def _extract_price(self, soup) -> Optional[float]:
        """Extract product price."""
        selectors = [
            '.x-price-primary span.ux-textspans',
            '[itemprop="price"]',
            '.mainPrice',
            '.notranslate.vi-VR-cvipPrice'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get('content') or element.get_text()
                return self.extract_price(price_text)
        return None

    def _extract_currency(self, soup) -> str:
        """Extract currency."""
        currency_element = soup.select_one('[itemprop="priceCurrency"]')
        if currency_element:
            return currency_element.get('content', 'USD')

        price_element = soup.select_one('.x-price-primary')
        if price_element:
            text = price_element.get_text()
            if '$' in text:
                return 'USD'
            elif '£' in text:
                return 'GBP'
            elif '€' in text:
                return 'EUR'
        return 'USD'

    def _extract_condition(self, soup) -> str:
        """Extract item condition."""
        condition_element = soup.select_one('.x-item-condition-text span')
        if condition_element:
            return self.clean_text(condition_element.get_text())

        condition_element = soup.select_one('[itemprop="itemCondition"]')
        if condition_element:
            return self.clean_text(condition_element.get_text())

        return "Unknown"

    def _extract_availability(self, soup) -> str:
        """Extract availability information."""
        availability_element = soup.select_one('.x-quantity__availability')
        if availability_element:
            return self.clean_text(availability_element.get_text())

        quantity_element = soup.select_one('#qtySubTxt span')
        if quantity_element:
            return self.clean_text(quantity_element.get_text())

        return "Check with seller"

    def _extract_seller(self, soup) -> str:
        """Extract seller name."""
        seller_element = soup.select_one('.x-sellercard-atf__info__about-seller a')
        if seller_element:
            return self.clean_text(seller_element.get_text())

        seller_element = soup.select_one('.mbg-nw')
        if seller_element:
            return self.clean_text(seller_element.get_text())

        return ""

    def _extract_seller_rating(self, soup) -> Optional[float]:
        """Extract seller feedback score."""
        rating_element = soup.select_one('.x-sellercard-atf__info__about-seller span')
        if rating_element:
            text = rating_element.get_text()
            import re
            match = re.search(r'([\d.]+)%', text)
            if match:
                return float(match.group(1))

        return None

    def _extract_images(self, soup) -> List[str]:
        """Extract product images."""
        images = []

        img_elements = soup.select('.ux-image-carousel-item img')
        for img in img_elements:
            src = img.get('src', '')
            if src and 'https://' in src:
                large_src = src.replace('s-l64', 's-l1600')
                images.append(large_src)

        main_image = soup.select_one('#icImg')
        if main_image and main_image.get('src'):
            images.insert(0, main_image['src'])

        return list(dict.fromkeys(images))[:15]

    def _extract_description(self, soup) -> str:
        """Extract product description."""
        desc_element = soup.select_one('#viTabs_0_panel')
        if desc_element:
            return self.clean_text(desc_element.get_text())

        desc_element = soup.select_one('.x-item-description')
        if desc_element:
            return self.clean_text(desc_element.get_text())

        return ""

    def _extract_item_specifics(self, soup) -> Dict[str, str]:
        """Extract item specifications."""
        specs = {}

        spec_rows = soup.select('.ux-layout-section--features .ux-labels-values')
        for row in spec_rows:
            label_elem = row.select_one('.ux-labels-values__labels')
            value_elem = row.select_one('.ux-labels-values__values')

            if label_elem and value_elem:
                key = self.clean_text(label_elem.get_text())
                value = self.clean_text(value_elem.get_text())
                specs[key] = value

        return specs

    def _extract_shipping(self, soup) -> str:
        """Extract shipping information."""
        shipping_element = soup.select_one('.ux-labels-values--shipping .ux-textspans')
        if shipping_element:
            return self.clean_text(shipping_element.get_text())

        shipping_element = soup.select_one('#fshippingCost')
        if shipping_element:
            return self.clean_text(shipping_element.get_text())

        return ""

    def _extract_watchers(self, soup) -> int:
        """Extract number of watchers."""
        watcher_element = soup.select_one('.vi-buybox-watchcount')
        if watcher_element:
            text = watcher_element.get_text()
            import re
            match = re.search(r'(\d+)', text.replace(',', ''))
            if match:
                return int(match.group(1))

        return 0

    def _extract_sold_count(self, soup) -> int:
        """Extract number of items sold."""
        sold_element = soup.select_one('.x-quantity__sold')
        if sold_element:
            text = sold_element.get_text()
            import re
            match = re.search(r'(\d+)', text.replace(',', ''))
            if match:
                return int(match.group(1))

        return 0

    def _extract_item_number(self, soup) -> str:
        """Extract eBay item number."""
        item_element = soup.select_one('[itemprop="productID"]')
        if item_element:
            return self.clean_text(item_element.get_text())

        import re
        item_match = re.search(r'itemId=(\d+)', soup.get_text())
        if item_match:
            return item_match.group(1)

        return ""
