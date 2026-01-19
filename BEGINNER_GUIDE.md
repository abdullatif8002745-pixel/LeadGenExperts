# Complete Beginner's Guide to Running the Web Scraper

This guide will help you run the e-commerce web scraper, even if you've never programmed before!

## 📋 What You Need

1. **A Computer** (Windows, Mac, or Linux)
2. **Internet Connection**
3. **15 minutes of your time**

That's it! Everything else we'll install together.

---

## 🪟 **For Windows Users**

### Step 1: Install Python

1. Go to https://www.python.org/downloads/
2. Click the big yellow button "Download Python 3.x.x"
3. Run the downloaded file
4. **IMPORTANT**: Check the box "Add Python to PATH" at the bottom
5. Click "Install Now"
6. Wait for installation to complete
7. Click "Close"

### Step 2: Download the Code

**Option A - If you have Git installed:**
1. Open Command Prompt (search "cmd" in Windows search)
2. Type these commands one by one:
```bash
cd Desktop
git clone https://github.com/abdullatif8002745-pixel/LeadGenExperts.git
cd LeadGenExperts
git checkout claude/document-capabilities-nYo5l
```

**Option B - Download as ZIP:**
1. Go to: https://github.com/abdullatif8002745-pixel/LeadGenExperts
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to your Desktop
5. Open Command Prompt and type:
```bash
cd Desktop\LeadGenExperts
```

### Step 3: Install Required Libraries

In Command Prompt, type these commands:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**What this does:**
- Creates a virtual environment (isolated space for this project)
- Activates it
- Installs all needed libraries

### Step 4: Run the Scraper!

**Test it first:**
```bash
python test_scraper.py
```

**Scrape a real product:**
```bash
python main.py --url "https://www.amazon.com/dp/B0BSHF7WHW" --format all
```

### Step 5: View Your Results

1. Open File Explorer
2. Go to the folder: `Desktop\LeadGenExperts\output`
3. You'll see files like:
   - `products_20260119_123456.json`
   - `products_20260119_123456.csv`
   - `products_20260119_123456.xlsx`
4. Open the Excel file to see your scraped data!

---

## 🍎 **For Mac Users**

### Step 1: Install Python

1. Open **Terminal** (search "Terminal" in Spotlight)
2. Check if Python is installed:
```bash
python3 --version
```

If you see "Python 3.x.x", you're good! If not:

3. Install Homebrew (package manager):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

4. Install Python:
```bash
brew install python3
```

### Step 2: Download the Code

**Option A - Using Git:**
```bash
cd ~/Desktop
git clone https://github.com/abdullatif8002745-pixel/LeadGenExperts.git
cd LeadGenExperts
git checkout claude/document-capabilities-nYo5l
```

**Option B - Download ZIP:**
1. Download from: https://github.com/abdullatif8002745-pixel/LeadGenExperts
2. Extract to Desktop
3. In Terminal:
```bash
cd ~/Desktop/LeadGenExperts
```

### Step 3: Install Required Libraries

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Run the Scraper!

**Test it:**
```bash
python test_scraper.py
```

**Scrape a product:**
```bash
python main.py --url "https://www.amazon.com/dp/B0BSHF7WHW" --format all
```

### Step 5: View Results

```bash
open output/
```

This opens the output folder with your scraped data!

---

## 🐧 **For Linux Users**

### Step 1: Install Python (if needed)

Open Terminal and run:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Step 2: Download the Code

```bash
cd ~/Desktop
git clone https://github.com/abdullatif8002745-pixel/LeadGenExperts.git
cd LeadGenExperts
git checkout claude/document-capabilities-nYo5l
```

### Step 3: Install Libraries

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Run the Scraper

```bash
python test_scraper.py
```

### Step 5: View Results

```bash
xdg-open output/
```

---

## 🎯 **Simple Examples You Can Try**

### Example 1: Scrape One Product

```bash
# Activate environment first (if not already active)
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Scrape an Amazon product
python main.py --url "https://www.amazon.com/dp/B0BSHF7WHW" --format json
```

### Example 2: Scrape Multiple Products

1. Create a text file named `my_products.txt` on your Desktop
2. Add product URLs (one per line):
```
https://www.amazon.com/dp/B0BSHF7WHW
https://www.amazon.com/dp/B08N5WRWNW
https://www.amazon.com/dp/B0C8PG85SL
```

3. Run the scraper:
```bash
python main.py --file my_products.txt --format all
```

### Example 3: Export to Excel Only

```bash
python main.py --url "YOUR_PRODUCT_URL" --format excel
```

---

## 📁 **Where to Find Your Scraped Data**

After running the scraper, look for the **output** folder:

- **Windows**: `C:\Users\YourName\Desktop\LeadGenExperts\output\`
- **Mac**: `/Users/YourName/Desktop/LeadGenExperts/output/`
- **Linux**: `/home/YourName/Desktop/LeadGenExperts/output/`

Inside you'll find:
- **.json files** - Raw data (for programmers)
- **.csv files** - Open with Excel/Google Sheets
- **.xlsx files** - Excel spreadsheets (easiest to read!)

---

## ❓ **Common Questions**

### Q: How do I find product URLs?

1. Go to Amazon, eBay, or any online store
2. Find a product you want to scrape
3. Copy the URL from your browser's address bar
4. Example: `https://www.amazon.com/dp/B0BSHF7WHW`

### Q: Can I scrape 100 products at once?

Yes! Create a text file with 100 URLs (one per line) and use:
```bash
python main.py --file your_file.txt --format all
```

### Q: How do I stop the scraper?

Press `Ctrl + C` (Windows/Linux) or `Cmd + C` (Mac)

### Q: How do I run it again?

Just run the same commands! Make sure to activate the virtual environment first:

**Windows:**
```bash
cd Desktop\LeadGenExperts
venv\Scripts\activate
python main.py --url "YOUR_URL" --format all
```

**Mac/Linux:**
```bash
cd ~/Desktop/LeadGenExperts
source venv/bin/activate
python main.py --url "YOUR_URL" --format all
```

---

## 🚨 **Troubleshooting**

### "Python is not recognized"
- **Fix**: Reinstall Python and CHECK the "Add to PATH" option

### "No module named 'requests'"
- **Fix**: Run `pip install -r requirements.txt` again

### "Permission denied"
- **Windows**: Run Command Prompt as Administrator
- **Mac/Linux**: Add `sudo` before the command

### "Failed to fetch URL"
- Check your internet connection
- Make sure the URL is correct
- Some websites block automated requests

### Virtual environment not working?
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 🎓 **Video Tutorial Suggestion**

If you prefer video tutorials, search YouTube for:
- "How to install Python on Windows/Mac"
- "How to run Python scripts"
- "Python virtual environment tutorial"

---

## 📞 **Need More Help?**

1. Read the `README.md` file in the project folder
2. Check `example.py` for code examples
3. Run `python main.py --help` to see all options

---

## ⚖️ **Legal & Ethical Use**

**Important Rules:**
- ✅ Only scrape websites you have permission to scrape
- ✅ Respect rate limits (don't scrape too fast)
- ✅ Check the website's Terms of Service
- ✅ Use scraped data responsibly
- ❌ Don't use this for spam or illegal activities
- ❌ Don't overload websites with requests

**This tool is for education and legitimate business use only!**

---

## 🎉 **You're Ready!**

Now you can scrape e-commerce websites like a pro! Start with the test script and work your way up to scraping hundreds of products.

Good luck! 🚀
