@echo off
echo ==========================================
echo Website Scraper - Starting Application
echo ==========================================
echo.

REM Check if credentials.json exists
if not exist "credentials.json" (
    echo Warning: credentials.json not found!
    echo Please follow the setup guide to create Google API credentials
    echo.
    set /p continue="Continue anyway? (y/n): "
    if /i not "%continue%"=="y" exit /b
)

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
)

REM Install requirements
echo Checking dependencies...
pip install -q -r requirements.txt

echo.
echo Starting Flask server...
echo The application will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ==========================================
echo.

REM Start the application
python app.py
