#!/bin/bash
# Quick Start Script for Mac/Linux
# Run this script to set up and test the scraper

echo "========================================"
echo "E-COMMERCE WEB SCRAPER - QUICK START"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo ""
    echo "Install Python:"
    echo "  Mac: brew install python3"
    echo "  Linux: sudo apt install python3 python3-pip python3-venv"
    echo ""
    exit 1
fi

echo "Step 1: Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created!"
else
    echo "Virtual environment already exists!"
fi
echo ""

echo "Step 2: Activating virtual environment..."
source venv/bin/activate
echo ""

echo "Step 3: Installing required libraries..."
pip install -r requirements.txt
echo ""

echo "Step 4: Running test scraper..."
echo ""
python test_scraper.py
echo ""

echo "========================================"
echo "SETUP COMPLETE!"
echo "========================================"
echo ""
echo "Your scraped data is in the 'test_output' folder."
echo ""
echo "To scrape your own products, use:"
echo "python main.py --url 'YOUR_PRODUCT_URL' --format all"
echo ""
