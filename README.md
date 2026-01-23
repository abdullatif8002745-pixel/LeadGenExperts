# Website Scraper - Lead Generation Tool

A powerful web scraping application that automatically extracts contact information from any website and saves it directly to Google Sheets.

## Features

- **Company Name Extraction**: Automatically identifies and extracts company names
- **Phone Number Detection**: Finds phone numbers from contact pages and footer sections
- **Email Discovery**: Extracts email addresses from contact pages and footers
- **Address Extraction**: Locates physical addresses from website content
- **Social Media Links**: Collects all social media profile links
- **Google Sheets Integration**: Automatically saves all data to Google Sheets without showing it to users
- **Clean UI**: Simple, user-friendly interface for entering website URLs

## Tech Stack

- **Backend**: Python, Flask
- **Web Scraping**: BeautifulSoup4, Requests
- **Google Sheets**: gspread, Google Auth
- **Frontend**: HTML, CSS, JavaScript

## Installation

### Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account
- Google Sheets API enabled

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd LeadGenExperts
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API and Google Drive API
4. Create a Service Account:
   - Go to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Give it a name and click "Create"
   - Grant it the "Editor" role
   - Click "Done"
5. Create a key for the service account:
   - Click on the service account you just created
   - Go to the "Keys" tab
   - Click "Add Key" > "Create New Key"
   - Choose "JSON" format
   - Download the JSON file
6. Rename the downloaded file to `credentials.json` and place it in the project root directory

### Step 4: Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your settings:
```
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_NAME=Lead Generation Data
```

### Step 5: Share Google Sheet (Optional)

If you want to access the Google Sheet from your personal account:
1. Open the `sheets_integration.py` file
2. Find the line with `spreadsheet.share()`
3. Uncomment it and add your email address

## Usage

### Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Enter a website URL in the input field and click "Start Scraping"

4. The application will:
   - Scrape the website for contact information
   - Extract company name, phone, email, address, and social links
   - Save the data directly to Google Sheets
   - Show a success message (without displaying the actual data)

### API Endpoints

#### POST /api/scrape
Initiates a scraping job for a given URL.

**Request Body:**
```json
{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "message": "Scraping started",
  "job_id": "unique-job-id"
}
```

#### GET /api/status/:job_id
Checks the status of a scraping job.

**Response:**
```json
{
  "status": "completed",
  "message": "Data successfully saved to Google Sheets!",
  "data": {
    "company_name": "Example Company"
  }
}
```

## Google Sheets Format

The data is saved to Google Sheets with the following columns:

| Timestamp | Company Name | Website URL | Phone Number | Email | Address | Social Links |
|-----------|--------------|-------------|--------------|-------|---------|--------------|
| 2025-01-23 10:30:45 | Example Corp | https://example.com | +1234567890 | info@example.com | 123 Main St | Facebook: https://facebook.com/example |

## How It Works

1. **URL Input**: User enters a website URL through the web interface
2. **Scraping Process**:
   - Fetches the main page content
   - Identifies and visits contact/about pages
   - Searches footer and contact sections
   - Extracts company name, phone, email, address, and social links
3. **Data Processing**: Validates and formats the extracted information
4. **Google Sheets Integration**: Saves data to Google Sheets with timestamp
5. **User Notification**: Shows success message without displaying the data

## Security Features

- Data is saved directly to Google Sheets without being displayed to users
- Uses Google Service Account authentication
- Environment variables for sensitive configuration
- CORS enabled for API security

## Troubleshooting

### "Credentials file not found" Error
- Make sure `credentials.json` is in the project root directory
- Verify the filename in `.env` matches your credentials file

### "Permission denied" Error
- Check that Google Sheets API and Drive API are enabled
- Verify the service account has proper permissions
- Make sure you've shared the spreadsheet with the service account email

### Scraping Returns "Not Found" for Most Fields
- Some websites block scraping attempts
- Try adding more diverse patterns in the scraper
- Check if the website has anti-scraping measures

## Development

### Project Structure

```
LeadGenExperts/
├── app.py                      # Flask application
├── scraper.py                  # Web scraping logic
├── sheets_integration.py       # Google Sheets integration
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── credentials.json           # Google Service Account credentials (not in repo)
├── templates/
│   └── index.html            # Web interface
└── README.md                 # Documentation
```

### Adding New Features

To add new extraction patterns:
1. Open `scraper.py`
2. Add new extraction methods in the `WebsiteScraper` class
3. Update the `scrape_website()` method to call your new extractors
4. Update `sheets_integration.py` to save the new fields

## License

MIT License - Feel free to use this project for your own purposes.

## Support

For issues or questions, please create an issue in the repository.
