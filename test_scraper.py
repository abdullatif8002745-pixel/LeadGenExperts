#!/usr/bin/env python3
"""
Quick test script for the E-commerce web scraper.
"""

from scraper import EcommerceScraper
from scraper.exporters import DataExporter
import json


def test_basic_scraping():
    """Test basic scraping with example URLs."""
    print("=" * 70)
    print("TESTING E-COMMERCE WEB SCRAPER")
    print("=" * 70)

    # Initialize scraper
    scraper = EcommerceScraper(rate_limit=2.0)
    exporter = DataExporter(output_dir="test_output")

    # Test URLs - you can replace these with actual product URLs
    test_urls = {
        "Amazon Example": "https://www.amazon.com/dp/B0BSHF7WHW",  # Echo Dot example
        "Generic Store": "https://example.com/product/test",  # Will fail but shows error handling
    }

    print("\n📦 Starting scraping tests...\n")

    products = []
    for name, url in test_urls.items():
        print(f"Testing: {name}")
        print(f"URL: {url}")
        print("-" * 70)

        try:
            product = scraper.scrape_product(url)

            if product and product.get('title'):
                print(f"✓ SUCCESS")
                print(f"  Platform: {product.get('platform', 'N/A')}")
                print(f"  Title: {product.get('title', 'N/A')[:60]}...")
                print(f"  Price: {product.get('currency', '')} {product.get('price', 'N/A')}")
                print(f"  Availability: {product.get('availability', 'N/A')}")

                products.append(product)
            else:
                print(f"✗ FAILED - No data extracted")

        except Exception as e:
            print(f"✗ ERROR - {e}")

        print()

    # Export results if we got any products
    if products:
        print("=" * 70)
        print(f"📊 EXPORTING {len(products)} PRODUCT(S)")
        print("=" * 70)

        try:
            # Export to JSON
            json_file = exporter.export_json(products, "test_products.json")
            print(f"✓ JSON: {json_file}")

            # Export to CSV
            csv_file = exporter.export_csv(products, "test_products.csv")
            print(f"✓ CSV: {csv_file}")

            # Export to Excel
            excel_file = exporter.export_excel(products, "test_products.xlsx")
            print(f"✓ Excel: {excel_file}")

            print("\n" + "=" * 70)
            print("✓ TEST COMPLETED SUCCESSFULLY!")
            print("=" * 70)

            # Display sample data
            print("\nSample Product Data:")
            print(json.dumps(products[0], indent=2, default=str)[:500] + "...")

        except Exception as e:
            print(f"✗ Export failed: {e}")
    else:
        print("=" * 70)
        print("⚠ No products were successfully scraped")
        print("=" * 70)
        print("\nTips for testing:")
        print("1. Replace test URLs with actual product URLs")
        print("2. Ensure you have internet connection")
        print("3. Some sites may block automated requests")
        print("4. Check the README.md for more examples")


if __name__ == "__main__":
    test_basic_scraping()
