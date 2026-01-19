"""
Shopify Store Scraper
Specialized scraper for Shopify-powered stores.
"""

import json
from typing import Dict, List, Optional
from ..base_scraper import BaseScraper


class ShopifyScraper(BaseScraper):
    """Scraper for Shopify-powered stores."""

    def scrape_product(self, url: str) -> Dict:
        """
        Scrape Shopify product information.

        Args:
            url: Shopify product URL

        Returns:
            Dictionary with product details
        """
        product_data = self._get_product_json(url)

        if product_data:
            return self._parse_json_data(product_data, url)

        html = self.fetch_page(url)
        if not html:
            return {}

        soup = self.parse_html(html)
        return self._parse_html_data(soup, url)

    def _get_product_json(self, url: str) -> Optional[Dict]:
        """
        Get product data from Shopify JSON endpoint.

        Shopify stores expose product data at /products/{handle}.json
        """
        if not url.endswith('.json'):
            if '/products/' in url:
                json_url = url.split('?')[0] + '.json'
            else:
                return None
        else:
            json_url = url

        html = self.fetch_page(json_url)
        if not html:
            return None

        try:
            data = json.loads(html)
            return data.get('product')
        except json.JSONDecodeError:
            return None

    def _parse_json_data(self, data: Dict, url: str) -> Dict:
        """Parse product data from JSON response."""
        variants = data.get('variants', [])
        first_variant = variants[0] if variants else {}

        images = [img['src'] for img in data.get('images', [])]

        product = {
            'url': url,
            'platform': 'shopify',
            'title': data.get('title', ''),
            'price': float(first_variant.get('price', 0)),
            'compare_at_price': self._get_compare_price(first_variant),
            'currency': self._detect_currency(first_variant.get('price', '0')),
            'availability': 'In Stock' if first_variant.get('available') else 'Out of Stock',
            'sku': first_variant.get('sku', ''),
            'vendor': data.get('vendor', ''),
            'product_type': data.get('product_type', ''),
            'tags': data.get('tags', []),
            'description': self.clean_text(data.get('body_html', '')),
            'images': images,
            'variants': self._parse_variants(variants),
            'options': data.get('options', []),
            'created_at': data.get('created_at', ''),
            'updated_at': data.get('updated_at', ''),
            'product_id': data.get('id', '')
        }

        return product

    def _parse_html_data(self, soup, url: str) -> Dict:
        """Fallback: Parse product data from HTML."""
        product = {
            'url': url,
            'platform': 'shopify',
            'title': self._extract_title(soup),
            'price': self._extract_price(soup),
            'currency': 'USD',
            'availability': self._extract_availability(soup),
            'vendor': self._extract_vendor(soup),
            'description': self._extract_description(soup),
            'images': self._extract_images(soup)
        }

        return product

    def _get_compare_price(self, variant: Dict) -> Optional[float]:
        """Extract compare at price (original price before discount)."""
        compare_price = variant.get('compare_at_price')
        if compare_price:
            try:
                return float(compare_price)
            except (ValueError, TypeError):
                pass
        return None

    def _detect_currency(self, price_str: str) -> str:
        """Detect currency from price string."""
        if isinstance(price_str, (int, float)):
            return 'USD'
        return 'USD'

    def _parse_variants(self, variants: List[Dict]) -> List[Dict]:
        """Parse product variants."""
        parsed_variants = []

        for variant in variants:
            parsed_variants.append({
                'id': variant.get('id'),
                'title': variant.get('title'),
                'price': float(variant.get('price', 0)),
                'sku': variant.get('sku', ''),
                'available': variant.get('available', False),
                'weight': variant.get('weight'),
                'weight_unit': variant.get('weight_unit'),
                'inventory_quantity': variant.get('inventory_quantity', 0),
                'option1': variant.get('option1'),
                'option2': variant.get('option2'),
                'option3': variant.get('option3')
            })

        return parsed_variants

    def _extract_title(self, soup) -> str:
        """Extract product title from HTML."""
        selectors = [
            'h1.product-title',
            'h1.product__title',
            '.product-single__title',
            'h1[itemprop="name"]'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return self.clean_text(element.get_text())
        return ""

    def _extract_price(self, soup) -> Optional[float]:
        """Extract price from HTML."""
        selectors = [
            '.product-price',
            '.price',
            '[itemprop="price"]',
            '.product__price'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get('content') or element.get_text()
                return self.extract_price(price_text)
        return None

    def _extract_availability(self, soup) -> str:
        """Extract availability from HTML."""
        availability_element = soup.select_one('.product-form__inventory')
        if availability_element:
            return self.clean_text(availability_element.get_text())

        add_to_cart = soup.select_one('button[name="add"]')
        if add_to_cart:
            if add_to_cart.get('disabled'):
                return 'Out of Stock'
            return 'In Stock'

        return 'Unknown'

    def _extract_vendor(self, soup) -> str:
        """Extract vendor/brand from HTML."""
        vendor_element = soup.select_one('.product__vendor')
        if vendor_element:
            return self.clean_text(vendor_element.get_text())

        vendor_element = soup.select_one('[itemprop="brand"]')
        if vendor_element:
            return self.clean_text(vendor_element.get_text())

        return ""

    def _extract_description(self, soup) -> str:
        """Extract description from HTML."""
        desc_element = soup.select_one('.product-single__description')
        if desc_element:
            return self.clean_text(desc_element.get_text())

        desc_element = soup.select_one('[itemprop="description"]')
        if desc_element:
            return self.clean_text(desc_element.get_text())

        return ""

    def _extract_images(self, soup) -> List[str]:
        """Extract images from HTML."""
        images = []

        img_elements = soup.select('.product__image img')
        for img in img_elements:
            src = img.get('src') or img.get('data-src')
            if src:
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    continue
                images.append(src)

        return list(dict.fromkeys(images))[:10]

    def scrape_category(self, url: str, max_products: int = 50) -> List[Dict]:
        """
        Scrape products from a Shopify collection page.

        Args:
            url: Collection URL
            max_products: Maximum number of products to scrape

        Returns:
            List of product dictionaries
        """
        if '/collections/' not in url:
            self.logger.warning("URL does not appear to be a collection page")
            return []

        json_url = url.split('?')[0] + '.json'
        html = self.fetch_page(json_url)

        if not html:
            return []

        try:
            data = json.loads(html)
            products_data = data.get('products', [])
        except json.JSONDecodeError:
            self.logger.error("Failed to parse collection JSON")
            return []

        products = []
        for product_data in products_data[:max_products]:
            product_url = f"{url.split('/collections/')[0]}/products/{product_data.get('handle')}"
            product = self._parse_json_data(product_data, product_url)
            products.append(product)

        return products
