# HexSoftwares Web Scraper

A production-ready Python web scraper for extracting book data from the "Books to Scrape" demo website. Built for HexSoftwares internship project.

## 🚀 Features

- **🖥️ Beautiful GUI Interface**: User-friendly interface with pastel colors and intuitive controls
- **💻 Command Line Interface**: Flexible CLI for advanced users and automation
- **Comprehensive Data Extraction**: Title, price, rating, availability, and product URLs
- **Deep Scraping**: Optional detailed product information (UPC, category, description)
- **Multiple Output Formats**: CSV and SQLite database support
- **Production Ready**: Error handling, retries, logging, and polite rate limiting
- **Real-time Progress**: Live progress bar and logging in GUI
- **macOS Compatible**: Tested on M1/M2 Macs

## 📋 Requirements

- Python 3.7+
- macOS (M1/M2 compatible)
- Internet connection

## 🛠️ Installation

1. **Clone or download the project**:
   ```bash
   cd HexSoftwares_WebScraper
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Quick Start

### 🖥️ GUI Interface (Recommended)
```bash
# Launch the beautiful GUI interface
python run_gui.py
```

### 💻 Command Line Interface
```bash
# Scrape 3 pages and save to CSV
python scrape_books.py

# Scrape 5 pages with detailed information
python scrape_books.py --max-pages 5 --deep

# Custom output files
python scrape_books.py --out-csv my_books.csv --out-sqlite books.db
```

### Advanced Usage
```bash
# Full featured scraping with custom settings
python scrape_books.py \
  --max-pages 10 \
  --delay 1.0 \
  --deep \
  --out-csv books_detailed.csv \
  --out-sqlite books_database.db \
  --log-level DEBUG
```

## 📊 CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--max-pages` | Maximum pages to scrape | 3 |
| `--delay` | Delay between requests (seconds) | 0.7 |
| `--deep` | Fetch detailed product information | False |
| `--out-csv` | CSV output filename | books.csv |
| `--out-sqlite` | SQLite output filename | None |
| `--log-level` | Logging level (DEBUG/INFO/WARNING/ERROR) | INFO |

## 📈 Sample Output

### CSV Format
```csv
title,price,rating,availability,product_url,upc,category,description
A Light in the Attic,£51.77,3,22,http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html,a90c9ac4,Poetry,"It's hard to imagine a world without A Light in the Attic..."
```

### Data Fields
- **title**: Book title
- **price**: Price in original currency
- **rating**: Star rating (1-5)
- **availability**: Number of books in stock
- **product_url**: Direct link to book page
- **upc**: Universal Product Code (deep mode only)
- **category**: Book category (deep mode only)
- **description**: Book description (deep mode only)

## 🏗️ Project Structure

```
HexSoftwares_WebScraper/
├── requirements.txt          # Python dependencies
├── scrape_books.py          # Main scraper script (CLI)
├── scraper_gui.py           # Beautiful GUI interface
├── run_gui.py              # GUI launcher script
├── README.md               # This file
└── .venv/                  # Virtual environment (created during setup)
```

## 🔧 Technical Details

### Architecture
- **Object-Oriented Design**: Clean, modular code with `BooksToScrapeScraper` class
- **Data Classes**: Type-safe data structures with `BookRow`
- **Error Handling**: Robust retry logic and graceful failure handling
- **Rate Limiting**: Polite scraping with configurable delays
- **Logging**: Comprehensive logging for debugging and monitoring

### Dependencies
- `requests`: HTTP client for web requests
- `beautifulsoup4`: HTML parsing and data extraction
- `lxml`: Fast XML/HTML parser

### Performance
- **Typical Speed**: ~2-3 books per second (with 0.7s delay)
- **Memory Efficient**: Processes books in batches
- **Network Friendly**: Respects robots.txt principles with delays

## 🧪 Testing

After running the scraper, you'll see sample output showing the first 5 books:

```
============================================================
SAMPLE DATA - First 5 rows
============================================================

📄 CSV Sample (books.csv):
  1. A Light in the Attic... | £51.77 | Rating: 3
  2. Tipping the Velvet... | £53.74 | Rating: 1
  3. Soumission... | £50.10 | Rating: 1
  4. Sharp Objects... | £47.82 | Rating: 4
  5. Sapiens: A Brief History... | £54.23 | Rating: 5

✅ Scraping completed successfully!
📊 Total books scraped: 50
📄 CSV file: books.csv
```

## 🚨 Troubleshooting

### Common Issues

1. **Connection Errors**: Check internet connection and try again
2. **Rate Limiting**: Increase `--delay` if getting blocked
3. **Permission Errors**: Ensure write permissions in the directory
4. **Import Errors**: Make sure virtual environment is activated

### Debug Mode
```bash
python scrape_books.py --log-level DEBUG
```

## 📝 License

This project is created for HexSoftwares internship purposes.

## 🤝 Contributing

This is an internship project. For questions or issues, please contact the development team.

---

**Built with ❤️ for HexSoftwares Internship**
