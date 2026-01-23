# Website Scraper - Complete Setup Guide

This guide will walk you through setting up the Website Scraper application step by step.

## Prerequisites Checklist

Before you begin, make sure you have:
- [ ] Python 3.8 or higher installed
- [ ] pip (Python package manager) installed
- [ ] A Google account
- [ ] Internet connection

## Step-by-Step Setup

### 1. Install Python Dependencies

Open your terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

Wait for all packages to install. This may take a few minutes.

### 2. Set Up Google Cloud Project

#### 2.1 Create a Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Click on the project dropdown at the top
3. Click "New Project"
4. Enter a project name (e.g., "Website Scraper")
5. Click "Create"
6. Wait for the project to be created and select it

#### 2.2 Enable Required APIs

1. In the Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Google Sheets API"
3. Click on it and click "Enable"
4. Go back to the library
5. Search for "Google Drive API"
6. Click on it and click "Enable"

#### 2.3 Create Service Account

1. Go to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account" at the top
3. Enter details:
   - **Service account name**: website-scraper
   - **Service account ID**: (auto-filled)
   - **Description**: Service account for website scraper application
4. Click "Create and Continue"
5. For "Grant this service account access to project":
   - Select role: "Editor"
   - Click "Continue"
6. Click "Done" (skip the optional steps)

#### 2.4 Create and Download Credentials

1. Find your newly created service account in the list
2. Click on it to open details
3. Go to the "Keys" tab
4. Click "Add Key" > "Create New Key"
5. Select "JSON" as the key type
6. Click "Create"
7. A JSON file will be downloaded to your computer
8. **Important**: Rename this file to `credentials.json`
9. Move `credentials.json` to your project root directory (same folder as app.py)

### 3. Configure Environment Variables

1. In your project directory, copy the example environment file:

```bash
# On Windows
copy .env.example .env

# On Mac/Linux
cp .env.example .env
```

2. Open the `.env` file in a text editor

3. Verify the settings:
```
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_NAME=Lead Generation Data
```

4. Save the file

### 4. (Optional) Share Google Sheet with Your Email

If you want to access the Google Sheet from your personal account:

1. Open `sheets_integration.py` in a text editor
2. Find this line (around line 50):
```python
# spreadsheet.share('your-email@example.com', perm_type='user', role='writer')
```

3. Uncomment it and replace with your email:
```python
spreadsheet.share('youremail@gmail.com', perm_type='user', role='writer')
```

4. Save the file

### 5. Test the Installation

Run a quick test to make sure everything is set up correctly:

```bash
python -c "import flask, bs4, gspread; print('All packages installed successfully!')"
```

If you see "All packages installed successfully!", you're good to go!

### 6. Run the Application

1. Start the Flask server:
```bash
python app.py
```

2. You should see output like:
```
 * Running on http://0.0.0.0:5000
 * Restarting with stat
 * Debugger is active!
```

3. Open your web browser and go to:
```
http://localhost:5000
```

4. You should see the Website Scraper interface!

## First Test

Let's test the scraper with a sample website:

1. In the URL input field, enter: `https://www.example.com`
2. Click "Start Scraping"
3. Wait for the process to complete
4. You should see a success message

5. Check your Google Sheets:
   - Go to https://docs.google.com/spreadsheets/
   - Look for a sheet named "Lead Generation Data"
   - You should see the scraped data in a new row!

## Troubleshooting

### Issue: "credentials.json not found"

**Solution:**
- Make sure the credentials.json file is in the same directory as app.py
- Check that the filename is exactly `credentials.json` (no extra spaces or characters)
- Verify the path in your .env file

### Issue: "Permission denied" when accessing Google Sheets

**Solution:**
- Make sure you enabled both Google Sheets API and Google Drive API
- Verify your service account has the "Editor" role
- Try creating a new service account key

### Issue: "ModuleNotFoundError"

**Solution:**
- Run `pip install -r requirements.txt` again
- Make sure you're using Python 3.8 or higher
- Try: `pip3 install -r requirements.txt`

### Issue: Port 5000 is already in use

**Solution:**
- Change the port in app.py:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Change to 5001 or any available port
```
- Then access the app at http://localhost:5001

### Issue: Website returns "Not Found" for all fields

**Solution:**
- Some websites block scraping attempts
- Try with different websites
- The scraper works best with business websites that have clear contact pages

## Security Best Practices

1. **Never commit credentials.json to version control**
   - Add it to .gitignore
   - Keep it secure on your local machine

2. **Limit service account permissions**
   - Only grant necessary permissions
   - Regularly review access

3. **Use environment variables**
   - Never hardcode sensitive information
   - Use the .env file for configuration

## Next Steps

Now that your scraper is set up:

1. Test it with various websites
2. Check the Google Sheet to see the collected data
3. Customize the scraper patterns in `scraper.py` for your specific needs
4. Add more extraction logic for additional fields

## Need Help?

If you encounter any issues:
1. Check the console output for error messages
2. Review the troubleshooting section above
3. Verify all setup steps were completed
4. Check that all files are in the correct locations

## File Checklist

Make sure you have all these files:

- [ ] app.py
- [ ] scraper.py
- [ ] sheets_integration.py
- [ ] requirements.txt
- [ ] .env
- [ ] credentials.json
- [ ] templates/index.html
- [ ] README.md

If any files are missing, refer to the README.md for the complete project structure.

---

Happy Scraping! 🚀
