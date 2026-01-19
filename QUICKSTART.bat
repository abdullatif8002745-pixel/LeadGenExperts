@echo off
REM Quick Start Script for Windows
REM Double-click this file to set up and run the scraper

echo ========================================
echo E-COMMERCE WEB SCRAPER - QUICK START
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Step 1: Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created!
) else (
    echo Virtual environment already exists!
)
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Step 3: Installing required libraries...
pip install -r requirements.txt
echo.

echo Step 4: Running test scraper...
echo.
python test_scraper.py
echo.

echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo Your scraped data is in the "test_output" folder.
echo.
echo To scrape your own products, use:
echo python main.py --url "YOUR_PRODUCT_URL" --format all
echo.
pause
