# Amazon Product Scraper

![Searching for Toast Maker](https://i.ibb.co/W4KS9VQd/searching-for-toast-maker.jpg)

## Overview

This is a simple Amazon product scraper that allows users to search for items on Amazon and extract product details. The project includes a graphical user interface (GUI) and supports downloading scraped data.

## Features

- Search for products on Amazon
- Extract item names, prices, ratings, and links
- Save the scraped data
- User-friendly GUI

## Files

- `main.py`: Entry point of the application
- `gui.py`: Contains the graphical user interface
- `amazonscrapper.py`: Core scraping logic
- `item.py`: Data model for product items
- `download.py`: Handles download functionality
- `.gitignore`: Standard Git ignore file

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`
- `tkinter`

Install dependencies using:

```bash
pip install requests beautifulsoup4
```

## Usage

Run the application with:

```bash
python main.py
```

Use the GUI to enter your search term and start scraping Amazon.

## Note

This scraper is for educational purposes. Be mindful of Amazon's terms of service regarding web scraping.
