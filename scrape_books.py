#!/usr/bin/env python3
"""
HexSoftwares Web Scraper
A production-ready web scraper for Books to Scrape website.
Extracts book data and saves to CSV and SQLite formats.
"""

import argparse
import csv
import logging
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


@dataclass
class BookRow:
    """Data class for book information."""
    title: str
    price: str
    rating: int
    availability: str
    product_url: str
    upc: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None


class BooksToScrapeScraper:
    """Main scraper class for Books to Scrape website."""
    
    def __init__(self, delay: float = 0.7, log_level: str = "INFO"):
        """Initialize the scraper with configuration."""
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        # Setup logging
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Rating mapping
        self.rating_map = {
            'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
        }
    
    def get_page(self, url: str, max_retries: int = 3) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page with retries."""
        for attempt in range(max_retries):
            try:
                self.logger.info(f"Fetching: {url} (attempt {attempt + 1})")
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'lxml')
                time.sleep(self.delay)  # Be polite
                return soup
                
            except requests.RequestException as e:
                self.logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    self.logger.error(f"Failed to fetch {url} after {max_retries} attempts")
                    return None
    
    def extract_rating(self, rating_class: str) -> int:
        """Convert rating class to numeric value."""
        for word, num in self.rating_map.items():
            if word.lower() in rating_class.lower():
                return num
        return 0
    
    def extract_availability(self, availability_text: str) -> str:
        """Extract quantity from availability text."""
        if 'In stock' in availability_text:
            # Extract number from text like "In stock (22 available)"
            import re
            match = re.search(r'\((\d+) available\)', availability_text)
            return match.group(1) if match else "Unknown"
        return "0"
    
    def scrape_book_listing(self, soup: BeautifulSoup, base_url: str) -> List[BookRow]:
        """Extract book data from a listing page."""
        books = []
        articles = soup.find_all('article', class_='product_pod')
        
        for article in articles:
            try:
                # Title and URL
                title_link = article.find('h3').find('a')
                title = title_link.get('title', '').strip()
                relative_url = title_link.get('href', '')
                product_url = urljoin(base_url, relative_url)
                
                # Price
                price_element = article.find('p', class_='price_color')
                price = price_element.text.strip() if price_element else "N/A"
                
                # Rating
                rating_element = article.find('p', class_='star-rating')
                rating_class = rating_element.get('class', []) if rating_element else []
                rating = self.extract_rating(' '.join(rating_class))
                
                # Availability
                availability_element = article.find('p', class_='instock availability')
                availability_text = availability_element.text.strip() if availability_element else ""
                availability = self.extract_availability(availability_text)
                
                books.append(BookRow(
                    title=title,
                    price=price,
                    rating=rating,
                    availability=availability,
                    product_url=product_url
                ))
                
            except Exception as e:
                self.logger.warning(f"Error parsing book: {e}")
                continue
        
        return books
    
    def scrape_book_detail(self, book: BookRow) -> BookRow:
        """Fetch additional details from product page."""
        soup = self.get_page(book.product_url)
        if not soup:
            return book
        
        try:
            # UPC
            upc_element = soup.find('th', string='UPC')
            upc = upc_element.find_next_sibling('td').text.strip() if upc_element else None
            
            # Category
            category_element = soup.find('ul', class_='breadcrumb').find_all('a')[-1]
            category = category_element.text.strip() if category_element else None
            
            # Description
            desc_element = soup.find('div', id='product_description')
            if desc_element:
                description = desc_element.find_next_sibling('p').text.strip()
            else:
                description = None
            
            # Update book with additional details
            book.upc = upc
            book.category = category
            book.description = description
            
        except Exception as e:
            self.logger.warning(f"Error fetching details for {book.title}: {e}")
        
        return book
    
    def scrape_books(self, max_pages: int = 3, deep: bool = False) -> List[BookRow]:
        """Main scraping method."""
        all_books = []
        base_url = "https://books.toscrape.com/catalogue/"
        
        for page_num in range(1, max_pages + 1):
            self.logger.info(f"Crawling page {page_num}...")
            url = f"{base_url}page-{page_num}.html"
            
            soup = self.get_page(url)
            if not soup:
                self.logger.error(f"Failed to fetch page {page_num}")
                continue
            
            books = self.scrape_book_listing(soup, base_url)
            self.logger.info(f"Found {len(books)} books on page {page_num}")
            
            # Fetch detailed information if requested
            if deep:
                self.logger.info("Fetching detailed information...")
                for i, book in enumerate(books):
                    self.logger.info(f"Fetching details for book {i+1}/{len(books)}: {book.title}")
                    books[i] = self.scrape_book_detail(book)
            
            all_books.extend(books)
        
        self.logger.info(f"Total books scraped: {len(all_books)}")
        return all_books
    
    def save_to_csv(self, books: List[BookRow], filename: str):
        """Save books data to CSV file."""
        self.logger.info(f"Saving {len(books)} books to {filename}")
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'price', 'rating', 'availability', 'product_url', 'upc', 'category', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for book in books:
                writer.writerow({
                    'title': book.title,
                    'price': book.price,
                    'rating': book.rating,
                    'availability': book.availability,
                    'product_url': book.product_url,
                    'upc': book.upc or '',
                    'category': book.category or '',
                    'description': book.description or ''
                })
        
        self.logger.info(f"CSV saved successfully: {filename}")
    
    def save_to_sqlite(self, books: List[BookRow], filename: str):
        """Save books data to SQLite database."""
        self.logger.info(f"Saving {len(books)} books to SQLite: {filename}")
        
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        
        # Create table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price TEXT,
                rating INTEGER,
                availability TEXT,
                product_url TEXT,
                upc TEXT,
                category TEXT,
                description TEXT
            )
        ''')
        
        # Insert data
        for book in books:
            cursor.execute('''
                INSERT INTO books (title, price, rating, availability, product_url, upc, category, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                book.title, book.price, book.rating, book.availability,
                book.product_url, book.upc, book.category, book.description
            ))
        
        conn.commit()
        conn.close()
        self.logger.info(f"SQLite database saved successfully: {filename}")


def print_sample_data(csv_file: str, sqlite_file: Optional[str] = None, limit: int = 5):
    """Print sample data from saved files."""
    print(f"\n{'='*60}")
    print(f"SAMPLE DATA - First {limit} rows")
    print(f"{'='*60}")
    
    # CSV sample
    if Path(csv_file).exists():
        print(f"\n📄 CSV Sample ({csv_file}):")
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= limit:
                    break
                print(f"  {i+1}. {row['title'][:50]}... | {row['price']} | Rating: {row['rating']}")
    
    # SQLite sample
    if sqlite_file and Path(sqlite_file).exists():
        print(f"\n🗄️  SQLite Sample ({sqlite_file}):")
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()
        cursor.execute('SELECT title, price, rating FROM books LIMIT ?', (limit,))
        rows = cursor.fetchall()
        for i, (title, price, rating) in enumerate(rows):
            print(f"  {i+1}. {title[:50]}... | {price} | Rating: {rating}")
        conn.close()


def main():
    """Main function with CLI argument parsing."""
    parser = argparse.ArgumentParser(description='HexSoftwares Web Scraper for Books to Scrape')
    parser.add_argument('--max-pages', type=int, default=3, help='Maximum pages to scrape (default: 3)')
    parser.add_argument('--delay', type=float, default=0.7, help='Delay between requests in seconds (default: 0.7)')
    parser.add_argument('--deep', action='store_true', help='Fetch detailed product information')
    parser.add_argument('--out-csv', default='books.csv', help='CSV output filename (default: books.csv)')
    parser.add_argument('--out-sqlite', help='SQLite output filename (optional)')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level (default: INFO)')
    
    args = parser.parse_args()
    
    # Initialize scraper
    scraper = BooksToScrapeScraper(delay=args.delay, log_level=args.log_level)
    
    # Scrape books
    books = scraper.scrape_books(max_pages=args.max_pages, deep=args.deep)
    
    if not books:
        print("No books were scraped. Check your internet connection and try again.")
        return
    
    # Save to files
    scraper.save_to_csv(books, args.out_csv)
    
    if args.out_sqlite:
        scraper.save_to_sqlite(books, args.out_sqlite)
    
    # Show sample data
    print_sample_data(args.out_csv, args.out_sqlite)
    
    print(f"\n✅ Scraping completed successfully!")
    print(f"📊 Total books scraped: {len(books)}")
    print(f"📄 CSV file: {args.out_csv}")
    if args.out_sqlite:
        print(f"🗄️  SQLite file: {args.out_sqlite}")


if __name__ == "__main__":
    main()

