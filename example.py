"""
Example usage of the E-commerce Web Scraper.
"""

from scraper import EcommerceScraper
from scraper.exporters import DataExporter


def example_single_product():
    """Example: Scrape a single product."""
    print("=" * 60)
    print("Example 1: Scraping a Single Product")
    print("=" * 60)

    scraper = EcommerceScraper(rate_limit=2.0)

    # Example URLs (replace with actual product URLs)
    url = "https://www.amazon.com/dp/B08N5WRWNW"  # Example Amazon product

    print(f"\nScraping: {url}")
    product = scraper.scrape_product(url)

    if product:
        print("\nProduct Information:")
        print(f"  Title: {product.get('title', 'N/A')}")
        print(f"  Price: {product.get('price', 'N/A')}")
        print(f"  Platform: {product.get('platform', 'N/A')}")
        print(f"  Availability: {product.get('availability', 'N/A')}")

        # Export to JSON
        exporter = DataExporter()
        json_file = exporter.export_json([product], "single_product.json")
        print(f"\nExported to: {json_file}")
    else:
        print("Failed to scrape product")


def example_multiple_products():
    """Example: Scrape multiple products from different platforms."""
    print("\n" + "=" * 60)
    print("Example 2: Scraping Multiple Products")
    print("=" * 60)

    scraper = EcommerceScraper(rate_limit=2.0)

    # Example URLs from different platforms
    urls = [
        "https://www.amazon.com/dp/B08N5WRWNW",
        "https://www.ebay.com/itm/123456789",
        # Add more URLs here
    ]

    print(f"\nScraping {len(urls)} products...")
    products = scraper.scrape_products(urls)

    print(f"\nSuccessfully scraped {len(products)} products")

    if products:
        # Export to all formats
        exporter = DataExporter()
        files = exporter.export_all(products, "multiple_products")

        print("\nExported to:")
        for format, filepath in files.items():
            print(f"  {format.upper()}: {filepath}")


def example_custom_export():
    """Example: Custom data export options."""
    print("\n" + "=" * 60)
    print("Example 3: Custom Export Options")
    print("=" * 60)

    scraper = EcommerceScraper(rate_limit=2.0)

    url = "https://www.amazon.com/dp/B08N5WRWNW"
    product = scraper.scrape_product(url)

    if product:
        exporter = DataExporter(output_dir="custom_output")

        # Export as pretty JSON
        json_file = exporter.export_json([product], pretty=True)
        print(f"Pretty JSON: {json_file}")

        # Export as CSV with flattened structure
        csv_file = exporter.export_csv([product], flatten=True)
        print(f"Flattened CSV: {csv_file}")

        # Export as Excel
        excel_file = exporter.export_excel([product])
        print(f"Excel file: {excel_file}")


def example_platform_specific():
    """Example: Using platform-specific scrapers directly."""
    print("\n" + "=" * 60)
    print("Example 4: Platform-Specific Scraping")
    print("=" * 60)

    from scraper.platforms import AmazonScraper, EbayScraper, ShopifyScraper

    # Amazon scraper
    amazon = AmazonScraper(rate_limit=2.0)
    amazon_url = "https://www.amazon.com/dp/B08N5WRWNW"
    amazon_product = amazon.scrape_product(amazon_url)
    print(f"Amazon Product: {amazon_product.get('title', 'N/A')}")

    # eBay scraper
    ebay = EbayScraper(rate_limit=2.0)
    ebay_url = "https://www.ebay.com/itm/123456789"
    ebay_product = ebay.scrape_product(ebay_url)
    print(f"eBay Product: {ebay_product.get('title', 'N/A')}")


def example_error_handling():
    """Example: Handling errors gracefully."""
    print("\n" + "=" * 60)
    print("Example 5: Error Handling")
    print("=" * 60)

    scraper = EcommerceScraper(rate_limit=1.0)

    urls = [
        "https://www.amazon.com/dp/B08N5WRWNW",
        "https://invalid-url-that-will-fail.com/product",
        "https://www.ebay.com/itm/123456789"
    ]

    products = []
    for url in urls:
        try:
            print(f"\nAttempting to scrape: {url}")
            product = scraper.scrape_product(url)
            if product:
                products.append(product)
                print(f"  ✓ Success: {product.get('title', 'N/A')[:50]}")
            else:
                print(f"  ✗ Failed to scrape")
        except Exception as e:
            print(f"  ✗ Error: {e}")

    print(f"\nTotal products scraped: {len(products)}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("E-COMMERCE WEB SCRAPER - EXAMPLES")
    print("=" * 60)

    # Run examples
    # Note: Uncomment the examples you want to run

    # example_single_product()
    # example_multiple_products()
    # example_custom_export()
    # example_platform_specific()
    # example_error_handling()

    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
    print("\nNote: Update the example URLs with actual product URLs to test.")
    print("Make sure to respect website terms of service and rate limits.")
