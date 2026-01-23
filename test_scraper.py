"""
Simple test script to verify the scraper is working
Run this to test the scraping functionality without starting the web server
"""

from scraper import scrape_url

def test_scraper():
    print("=" * 60)
    print("Website Scraper - Test Script")
    print("=" * 60)
    print()

    # Test URL - you can change this to any website
    test_url = "https://www.example.com"

    print(f"Testing scraper with URL: {test_url}")
    print()
    print("Scraping in progress...")
    print("-" * 60)

    try:
        # Scrape the website
        results = scrape_url(test_url)

        # Display results
        print("\n✓ Scraping completed successfully!\n")
        print("Results:")
        print("-" * 60)
        print(f"Company Name:   {results['company_name']}")
        print(f"Phone Number:   {results['phone']}")
        print(f"Email:          {results['email']}")
        print(f"Address:        {results['address']}")
        print(f"Social Links:   {results['social_links']}")
        print("-" * 60)

        print("\nNote: This is just a test. To save to Google Sheets,")
        print("run the full application with: python app.py")

    except Exception as e:
        print(f"\n✗ Error occurred: {str(e)}")
        print("\nPlease check:")
        print("1. You have internet connection")
        print("2. The URL is valid and accessible")
        print("3. All required packages are installed")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_scraper()
