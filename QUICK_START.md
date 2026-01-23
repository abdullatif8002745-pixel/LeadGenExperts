# Quick Start Guide

Get up and running with the Website Scraper in 5 minutes!

## Prerequisites

- Python 3.8+
- Google account

## Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "Google Sheets API" and "Google Drive API"
4. Create a Service Account with "Editor" role
5. Download the JSON key as `credentials.json`
6. Place `credentials.json` in the project root

### 3. Configure Environment

```bash
cp .env.example .env
```

### 4. Run the Application

**Linux/Mac:**
```bash
./start.sh
```

**Windows:**
```bash
start.bat
```

**Or manually:**
```bash
python app.py
```

### 5. Access the Application

Open your browser and go to:
```
http://localhost:5000
```

## Usage

1. Enter a website URL (e.g., `https://example.com`)
2. Click "Start Scraping"
3. Wait for completion
4. Check your Google Sheets for the data!

## What Gets Scraped?

- ✓ Company Name
- ✓ Phone Number (from contact/footer)
- ✓ Email Address (from contact/footer)
- ✓ Physical Address
- ✓ Social Media Links

## Where is the Data?

The scraped data is automatically saved to a Google Sheet named **"Lead Generation Data"**.

- Go to [Google Sheets](https://docs.google.com/spreadsheets/)
- Find "Lead Generation Data"
- View all scraped data with timestamps

## Test Without Google Sheets

Run the test script to verify scraping works:
```bash
python test_scraper.py
```

## Troubleshooting

**Can't find credentials.json?**
- Make sure you downloaded it from Google Cloud Console
- Place it in the same folder as `app.py`

**Port 5000 already in use?**
- Edit `app.py` and change the port number
- Or kill the process using port 5000

**"Module not found" error?**
- Run: `pip install -r requirements.txt`
- Make sure you're using Python 3.8+

## Need More Help?

- Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions
- Check [README.md](README.md) for complete documentation

---

Happy Scraping! 🚀
