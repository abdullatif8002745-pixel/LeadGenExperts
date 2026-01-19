# E-commerce Web Scraper

A comprehensive, feature-rich web scraper for extracting product information from various e-commerce platforms including Amazon, eBay, Shopify stores, and more.

## Features

### Supported Platforms
- **Amazon** - Complete product details including ASIN, reviews, ratings, specifications
- **eBay** - Listings with seller information, item specifics, and condition
- **Shopify** - Products from any Shopify-powered store with variants and options
- **Generic** - Fallback scraper for any other e-commerce platform using common patterns

### Product Information Extracted
- Title, price, and currency
- Product images (high-resolution)
- Detailed descriptions and features
- Specifications and attributes
- Availability and stock status
- Ratings and review counts
- Brand and category information
- Platform-specific data (ASIN, SKU, etc.)

### Export Formats
- **JSON** - Structured data with full details
- **CSV** - Tabular format for spreadsheet analysis
- **Excel** - Formatted spreadsheets with auto-sized columns
- **All formats** - Export to all formats simultaneously

### Key Features
- **Auto-detection** - Automatically detects the e-commerce platform
- **Rate limiting** - Respects websites with configurable delays between requests
- **Random user agents** - Rotates user agents to avoid blocking
- **Error handling** - Robust retry logic and graceful error handling
- **Multiple products** - Batch scraping from multiple URLs
- **Logging** - Detailed logging for monitoring and debugging

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. **Clone or download this repository**
```bash
cd LeadGenExperts
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure (optional)**
```bash
cp .env.example .env
# Edit .env with your preferred settings
```

## Usage

### Command Line Interface

#### Scrape a single product
```bash
python main.py --url "https://www.amazon.com/dp/B08N5WRWNW"
```

#### Scrape multiple products
```bash
python main.py --urls "url1" "url2" "url3" --format csv
```

#### Scrape from a file
Create a text file `urls.txt` with one URL per line:
```
https://www.amazon.com/dp/B08N5WRWNW
https://www.ebay.com/itm/123456789
https://example.myshopify.com/products/example
```

Then run:
```bash
python main.py --file urls.txt --format excel
```

#### Export to all formats
```bash
python main.py --url "https://example.com/product" --format all
```

#### Custom output directory and rate limit
```bash
python main.py --url "https://example.com/product" --output data --rate-limit 3.0
```

### Python API

#### Basic Usage
```python
from scraper import EcommerceScraper
from scraper.exporters import DataExporter

# Initialize scraper
scraper = EcommerceScraper(rate_limit=2.0)

# Scrape a single product
product = scraper.scrape_product("https://www.amazon.com/dp/B08N5WRWNW")

# Export to JSON
exporter = DataExporter()
exporter.export_json([product], "product.json")
```

#### Scrape Multiple Products
```python
urls = [
    "https://www.amazon.com/dp/B08N5WRWNW",
    "https://www.ebay.com/itm/123456789",
    "https://example.myshopify.com/products/product-name"
]

products = scraper.scrape_products(urls)

# Export to all formats
exporter = DataExporter()
files = exporter.export_all(products, prefix="my_products")
```

#### Platform-Specific Scraping
```python
from scraper.platforms import AmazonScraper, EbayScraper, ShopifyScraper

# Use platform-specific scraper directly
amazon = AmazonScraper(rate_limit=2.0)
product = amazon.scrape_product("https://www.amazon.com/dp/B08N5WRWNW")
```

#### Custom Export Options
```python
from scraper.exporters import DataExporter

exporter = DataExporter(output_dir="custom_output")

# Pretty JSON
exporter.export_json(products, "products.json", pretty=True)

# Flattened CSV
exporter.export_csv(products, "products.csv", flatten=True)

# Excel with auto-sized columns
exporter.export_excel(products, "products.xlsx")
```

## Examples

See `example.py` for more detailed usage examples:
```bash
python example.py
```

## Project Structure

```
LeadGenExperts/
├── scraper/
│   ├── __init__.py
│   ├── base_scraper.py          # Base scraper with common functionality
│   ├── ecommerce_scraper.py     # Main scraper with auto-detection
│   ├── platforms/               # Platform-specific scrapers
│   │   ├── __init__.py
│   │   ├── amazon_scraper.py
│   │   ├── ebay_scraper.py
│   │   ├── shopify_scraper.py
│   │   └── generic_scraper.py
│   └── exporters/               # Data export functionality
│       ├── __init__.py
│       └── data_exporter.py
├── main.py                      # CLI interface
├── example.py                   # Usage examples
├── requirements.txt             # Python dependencies
├── .env.example                 # Configuration template
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Configuration

Create a `.env` file from `.env.example` to customize settings:

```env
# Scraping Settings
RATE_LIMIT=2.0
USE_SELENIUM=false

# Output Settings
OUTPUT_DIR=output
DEFAULT_FORMAT=json

# Logging
LOG_LEVEL=INFO
```

## CLI Options

```
python main.py --help

Options:
  -h, --help            Show help message
  --url URL             Single product URL to scrape
  --urls URL [URL ...]  Multiple product URLs to scrape
  --file FILE           Text file containing URLs (one per line)
  --format {json,csv,excel,all}
                        Output format (default: json)
  --output OUTPUT       Output directory (default: output)
  --rate-limit RATE     Minimum seconds between requests (default: 2.0)
  --selenium            Use Selenium for dynamic content
```

## Best Practices

1. **Respect robots.txt** - Always check the website's robots.txt file
2. **Use appropriate rate limits** - Don't overload servers (2-3 seconds recommended)
3. **User agent rotation** - Enabled by default to avoid blocks
4. **Error handling** - The scraper includes retry logic and graceful failures
5. **Legal compliance** - Ensure you have permission to scrape and comply with terms of service

## Limitations

- Some websites use advanced bot detection (Cloudflare, PerimeterX, etc.)
- Dynamic content may require Selenium (not fully implemented)
- Product structures vary widely across platforms
- Rate limits are essential to avoid IP bans

## Troubleshooting

### "Failed to fetch" errors
- Check your internet connection
- The URL might be invalid or the product removed
- Website might be blocking automated requests
- Try increasing rate limit: `--rate-limit 5.0`

### Missing data in exports
- Some fields may not be available on all platforms
- Generic scraper may not capture all platform-specific fields
- Try using platform-specific scrapers directly

### Import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Activate your virtual environment if using one

## Legal Disclaimer

This tool is for educational purposes only. Users are responsible for:
- Complying with website terms of service
- Respecting robots.txt files
- Following applicable laws and regulations
- Not using this tool for unauthorized data collection

Web scraping may be against the terms of service of some websites. Always obtain permission before scraping and use responsibly.

## Contributing

Contributions are welcome! Areas for improvement:
- Additional platform scrapers (Walmart, AliExpress, etc.)
- Selenium integration for JavaScript-heavy sites
- Proxy support for IP rotation
- Multi-threading for faster scraping
- API integrations as alternatives to scraping

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions:
1. Check existing documentation
2. Review example.py for usage patterns
3. Open an issue with detailed information

## Changelog

### Version 1.0.0
- Initial release
- Support for Amazon, eBay, Shopify, and generic platforms
- JSON, CSV, and Excel export formats
- CLI interface and Python API
- Rate limiting and error handling
- Comprehensive documentation

## Acknowledgments

Built with:
- BeautifulSoup4 for HTML parsing
- Requests for HTTP requests
- Pandas for data manipulation
- Selenium for dynamic content (optional)

---

**Remember:** Always scrape responsibly and ethically!
