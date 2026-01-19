"""
Generic E-commerce Scraper
Fallback scraper for any e-commerce platform using common patterns.
"""

from typing import Dict, List, Optional
from ..base_scraper import BaseScraper


class GenericScraper(BaseScraper):
    """Generic scraper for any e-commerce site using common HTML patterns."""

    def scrape_product(self, url: str) -> Dict:
        """
        Scrape product information using generic selectors.

        Args:
            url: Product URL

        Returns:
            Dictionary with product details
        """
        html = self.fetch_page(url)
        if not html:
            return {}

        soup = self.parse_html(html)

        product = {
            'url': url,
            'platform': 'generic',
            'title': self._extract_title(soup),
            'price': self._extract_price(soup),
            'currency': self._extract_currency(soup),
            'description': self._extract_description(soup),
            'images': self._extract_images(soup),
            'availability': self._extract_availability(soup),
            'brand': self._extract_brand(soup),
            'rating': self._extract_rating(soup),
            'structured_data': self._extract_structured_data(soup)
        }

        return product

    def _extract_title(self, soup) -> str:
        """Extract product title using common patterns."""
        selectors = [
            'h1[itemprop="name"]',
            'h1.product-title',
            'h1.product-name',
            'h1.product_title',
            'h1.productName',
            '.product-title h1',
            '.product-name h1',
            'h1'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                title = self.clean_text(element.get_text())
                if len(title) > 10:
                    return title

        og_title = soup.find('meta', property='og:title')
        if og_title:
            return og_title.get('content', '')

        return ""

    def _extract_price(self, soup) -> Optional[float]:
        """Extract price using common patterns."""
        selectors = [
            '[itemprop="price"]',
            '.price',
            '.product-price',
            '.productPrice',
            '.sale-price',
            '.current-price',
            'span.price',
            '.price-now'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get('content') or element.get_text()
                price = self.extract_price(price_text)
                if price:
                    return price

        return None

    def _extract_currency(self, soup) -> str:
        """Extract currency."""
        currency_element = soup.select_one('[itemprop="priceCurrency"]')
        if currency_element:
            return currency_element.get('content', 'USD')

        price_elements = soup.select('.price, .product-price')
        for elem in price_elements:
            text = elem.get_text()
            if '$' in text:
                return 'USD'
            elif '£' in text:
                return 'GBP'
            elif '€' in text:
                return 'EUR'
            elif '¥' in text:
                return 'JPY'

        return 'USD'

    def _extract_description(self, soup) -> str:
        """Extract product description."""
        selectors = [
            '[itemprop="description"]',
            '.product-description',
            '.productDescription',
            '.description',
            '#description',
            '.product-details',
            '.product-info'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                desc = self.clean_text(element.get_text())
                if len(desc) > 20:
                    return desc

        og_desc = soup.find('meta', property='og:description')
        if og_desc:
            return og_desc.get('content', '')

        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            return meta_desc.get('content', '')

        return ""

    def _extract_images(self, soup) -> List[str]:
        """Extract product images."""
        images = []

        img_selectors = [
            '[itemprop="image"]',
            '.product-image img',
            '.productImage img',
            '.gallery img',
            '#product-image',
            '.main-image img'
        ]

        for selector in img_selectors:
            elements = soup.select(selector)
            for elem in elements:
                src = elem.get('src') or elem.get('data-src') or elem.get('data-lazy')
                if src:
                    if src.startswith('//'):
                        src = 'https:' + src
                    elif src.startswith('/'):
                        continue
                    if 'http' in src:
                        images.append(src)

        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            images.insert(0, og_image['content'])

        return list(dict.fromkeys(images))[:10]

    def _extract_availability(self, soup) -> str:
        """Extract availability status."""
        selectors = [
            '[itemprop="availability"]',
            '.availability',
            '.stock-status',
            '.in-stock',
            '.out-of-stock'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return self.clean_text(element.get_text())

        add_to_cart = soup.select_one('button.add-to-cart, button[type="submit"]')
        if add_to_cart:
            if add_to_cart.get('disabled'):
                return 'Out of Stock'
            button_text = add_to_cart.get_text().lower()
            if 'add to cart' in button_text or 'buy now' in button_text:
                return 'In Stock'

        return 'Unknown'

    def _extract_brand(self, soup) -> str:
        """Extract brand name."""
        selectors = [
            '[itemprop="brand"]',
            '.brand',
            '.product-brand',
            '.manufacturer'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                brand = self.clean_text(element.get_text())
                if brand:
                    return brand

        return ""

    def _extract_rating(self, soup) -> Optional[float]:
        """Extract product rating."""
        rating_element = soup.select_one('[itemprop="ratingValue"]')
        if rating_element:
            rating_text = rating_element.get('content') or rating_element.get_text()
            try:
                return float(rating_text)
            except ValueError:
                pass

        rating_selectors = [
            '.rating',
            '.product-rating',
            '.star-rating'
        ]

        for selector in rating_selectors:
            element = soup.select_one(selector)
            if element:
                import re
                text = element.get_text()
                match = re.search(r'([\d.]+)', text)
                if match:
                    try:
                        return float(match.group(1))
                    except ValueError:
                        pass

        return None

    def _extract_structured_data(self, soup) -> Dict:
        """Extract JSON-LD structured data."""
        import json

        scripts = soup.find_all('script', type='application/ld+json')

        for script in scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and data.get('@type') == 'Product':
                    return data
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and item.get('@type') == 'Product':
                            return item
            except (json.JSONDecodeError, AttributeError):
                continue

        return {}
