import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class GoogleSheetsManager:
    def __init__(self):
        self.credentials_file = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE', 'credentials.json')
        self.sheet_name = os.getenv('GOOGLE_SHEET_NAME', 'Lead Generation Data')
        self.client = None
        self.worksheet = None

    def authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            # Define the scope
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]

            # Create credentials
            creds = Credentials.from_service_account_file(
                self.credentials_file,
                scopes=scopes
            )

            # Authorize the client
            self.client = gspread.authorize(creds)
            print("Successfully authenticated with Google Sheets")
            return True

        except FileNotFoundError:
            print(f"Error: Credentials file '{self.credentials_file}' not found")
            return False
        except Exception as e:
            print(f"Error authenticating: {str(e)}")
            return False

    def get_or_create_sheet(self):
        """Get existing spreadsheet or create a new one"""
        try:
            # Try to open existing spreadsheet
            spreadsheet = self.client.open(self.sheet_name)
            self.worksheet = spreadsheet.sheet1
            print(f"Opened existing spreadsheet: {self.sheet_name}")

        except gspread.SpreadsheetNotFound:
            # Create new spreadsheet
            print(f"Creating new spreadsheet: {self.sheet_name}")
            spreadsheet = self.client.create(self.sheet_name)

            # Share with your email (optional - update with your email)
            # spreadsheet.share('your-email@example.com', perm_type='user', role='writer')

            self.worksheet = spreadsheet.sheet1

            # Set up headers
            headers = [
                'Timestamp',
                'Company Name',
                'Website URL',
                'Phone Number',
                'Email',
                'Address',
                'Social Links'
            ]
            self.worksheet.update('A1:G1', [headers])

            # Format header row
            self.worksheet.format('A1:G1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.2, 'green': 0.2, 'blue': 0.8}
            })

        return True

    def save_data(self, data):
        """Save scraped data to Google Sheets"""
        try:
            if not self.client:
                self.authenticate()

            if not self.worksheet:
                self.get_or_create_sheet()

            # Prepare row data
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            row_data = [
                timestamp,
                data.get('company_name', 'Not Found'),
                data.get('url', ''),
                data.get('phone', 'Not Found'),
                data.get('email', 'Not Found'),
                data.get('address', 'Not Found'),
                data.get('social_links', 'Not Found')
            ]

            # Append the row
            self.worksheet.append_row(row_data)
            print(f"Data saved to Google Sheets: {data.get('company_name', 'Unknown')}")

            return True

        except Exception as e:
            print(f"Error saving to Google Sheets: {str(e)}")
            return False

    def get_all_data(self):
        """Retrieve all data from the sheet (for testing purposes)"""
        try:
            if not self.client:
                self.authenticate()

            if not self.worksheet:
                self.get_or_create_sheet()

            return self.worksheet.get_all_records()

        except Exception as e:
            print(f"Error retrieving data: {str(e)}")
            return []


def save_to_sheets(scraped_data):
    """Helper function to save data to Google Sheets"""
    sheets_manager = GoogleSheetsManager()

    if sheets_manager.authenticate():
        sheets_manager.get_or_create_sheet()
        return sheets_manager.save_data(scraped_data)

    return False
