#!/bin/bash

echo "=========================================="
echo "Website Scraper - Starting Application"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if credentials.json exists
if [ ! -f "credentials.json" ]; then
    echo "Warning: credentials.json not found!"
    echo "Please follow the setup guide to create Google API credentials"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        exit 1
    fi
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
fi

# Install requirements if needed
echo "Checking dependencies..."
pip3 install -q -r requirements.txt

echo ""
echo "Starting Flask server..."
echo "The application will be available at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Start the application
python3 app.py
