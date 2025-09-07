#!/usr/bin/env python3
"""
HexSoftwares Web Scraper - GUI Interface
A beautiful, user-friendly GUI for the Books to Scrape web scraper.
Features pastel colors and intuitive controls.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import os
import sys
from pathlib import Path
import webbrowser

# Import our scraper
from scrape_books import BooksToScrapeScraper, print_sample_data


class ScraperGUI:
    """Main GUI class for the web scraper."""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.scraper = None
        self.is_running = False
        
    def setup_window(self):
        """Configure the main window."""
        self.root.title("HexSoftwares Web Scraper")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"800x700+{x}+{y}")
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def setup_styles(self):
        """Setup pastel color theme and styles."""
        self.colors = {
            'bg_primary': '#E6F3FF',      # Light blue
            'bg_secondary': '#D1ECF1',    # Soft blue
            'accent_1': '#B8D4F0',        # Light blue accent
            'accent_2': '#D4EDDA',        # Soft green
            'accent_3': '#F8D7DA',        # Soft pink
            'accent_4': '#FFF3CD',        # Soft yellow
            'text_primary': '#495057',    # Dark gray
            'text_secondary': '#6C757D',  # Medium gray
            'button_bg': '#A8DADC',       # Pastel blue
            'button_hover': '#457B9D',    # Darker blue
            'success': '#28A745',         # Green
            'warning': '#FFC107',         # Yellow
            'error': '#DC3545'            # Red
        }
        
        # Configure root background
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Pastel.TButton',
                       background=self.colors['button_bg'],
                       foreground=self.colors['text_primary'],
                       font=('SF Pro Display', 10, 'bold'),
                       padding=(10, 8))
        
        style.map('Pastel.TButton',
                 background=[('active', self.colors['button_hover']),
                           ('pressed', self.colors['button_hover'])])
        
        # Configure frame styles
        style.configure('Card.TFrame',
                       background=self.colors['bg_secondary'],
                       relief='raised',
                       borderwidth=1)
        
        # Configure label styles
        style.configure('Title.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=('SF Pro Display', 16, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_secondary'],
                       font=('SF Pro Display', 12))
        
    def create_widgets(self):
        """Create and arrange all GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, style='Card.TFrame', padding=20)
        main_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        self.create_header(main_frame)
        
        # Content area
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=1, column=0, sticky='nsew', pady=(20, 0))
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Left panel - Controls
        self.create_controls_panel(content_frame)
        
        # Right panel - Output
        self.create_output_panel(content_frame)
        
        # Footer
        self.create_footer(main_frame)
        
    def create_header(self, parent):
        """Create the header section."""
        header_frame = ttk.Frame(parent, style='Card.TFrame')
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(header_frame, 
                               text="HexSoftwares Web Scraper",
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame,
                                  text="Extract book data from Books to Scrape website",
                                  style='Subtitle.TLabel')
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
    def create_controls_panel(self, parent):
        """Create the controls panel."""
        controls_frame = ttk.LabelFrame(parent, text="Scraping Options", 
                                       style='Card.TFrame', padding=15)
        controls_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        # Max Pages
        ttk.Label(controls_frame, text="Max Pages:", 
                 font=('SF Pro Display', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        self.max_pages_var = tk.StringVar(value="3")
        max_pages_spinbox = ttk.Spinbox(controls_frame, from_=1, to=50, 
                                       textvariable=self.max_pages_var, width=10)
        max_pages_spinbox.grid(row=0, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # Delay
        ttk.Label(controls_frame, text="Delay (seconds):", 
                 font=('SF Pro Display', 10, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        self.delay_var = tk.StringVar(value="0.7")
        delay_spinbox = ttk.Spinbox(controls_frame, from_=0.1, to=5.0, increment=0.1,
                                   textvariable=self.delay_var, width=10)
        delay_spinbox.grid(row=1, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # Deep Scraping
        self.deep_var = tk.BooleanVar()
        deep_check = ttk.Checkbutton(controls_frame, text="Deep Scraping (UPC, Category, Description)",
                                    variable=self.deep_var)
        deep_check.grid(row=2, column=0, columnspan=2, sticky='w', pady=10)
        
        # Log Level
        ttk.Label(controls_frame, text="Log Level:", 
                 font=('SF Pro Display', 10, 'bold')).grid(row=3, column=0, sticky='w', pady=5)
        self.log_level_var = tk.StringVar(value="INFO")
        log_level_combo = ttk.Combobox(controls_frame, textvariable=self.log_level_var,
                                      values=["DEBUG", "INFO", "WARNING", "ERROR"], 
                                      state="readonly", width=8)
        log_level_combo.grid(row=3, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # Output Options
        ttk.Label(controls_frame, text="Output Options:", 
                 font=('SF Pro Display', 10, 'bold')).grid(row=4, column=0, columnspan=2, sticky='w', pady=(15, 5))
        
        # CSV Output
        csv_frame = ttk.Frame(controls_frame)
        csv_frame.grid(row=5, column=0, columnspan=2, sticky='ew', pady=2)
        csv_frame.grid_columnconfigure(1, weight=1)
        
        self.csv_var = tk.BooleanVar(value=True)
        csv_check = ttk.Checkbutton(csv_frame, text="CSV File:", variable=self.csv_var)
        csv_check.grid(row=0, column=0, sticky='w')
        
        self.csv_filename_var = tk.StringVar(value="books.csv")
        csv_entry = ttk.Entry(csv_frame, textvariable=self.csv_filename_var, width=20)
        csv_entry.grid(row=0, column=1, sticky='ew', padx=(10, 5))
        
        csv_browse_btn = ttk.Button(csv_frame, text="Browse", width=8,
                                   command=self.browse_csv_file)
        csv_browse_btn.grid(row=0, column=2)
        
        # SQLite Output
        sqlite_frame = ttk.Frame(controls_frame)
        sqlite_frame.grid(row=6, column=0, columnspan=2, sticky='ew', pady=2)
        sqlite_frame.grid_columnconfigure(1, weight=1)
        
        self.sqlite_var = tk.BooleanVar()
        sqlite_check = ttk.Checkbutton(sqlite_frame, text="SQLite Database:", variable=self.sqlite_var)
        sqlite_check.grid(row=0, column=0, sticky='w')
        
        self.sqlite_filename_var = tk.StringVar(value="books.db")
        sqlite_entry = ttk.Entry(sqlite_frame, textvariable=self.sqlite_filename_var, width=20)
        sqlite_entry.grid(row=0, column=1, sticky='ew', padx=(10, 5))
        
        sqlite_browse_btn = ttk.Button(sqlite_frame, text="Browse", width=8,
                                      command=self.browse_sqlite_file)
        sqlite_browse_btn.grid(row=0, column=2)
        
        # Control Buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=(20, 0))
        
        self.start_btn = ttk.Button(button_frame, text="Start Scraping", 
                                   style='Pastel.TButton', command=self.start_scraping)
        self.start_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_btn = ttk.Button(button_frame, text="Stop", 
                                  style='Pastel.TButton', command=self.stop_scraping,
                                  state='disabled')
        self.stop_btn.grid(row=0, column=1)
        
        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(controls_frame, variable=self.progress_var,
                                           maximum=100, length=200)
        self.progress_bar.grid(row=8, column=0, columnspan=2, sticky='ew', pady=(15, 0))
        
    def create_output_panel(self, parent):
        """Create the output panel."""
        output_frame = ttk.LabelFrame(parent, text="Output & Logs", 
                                     style='Card.TFrame', padding=15)
        output_frame.grid(row=0, column=1, sticky='nsew')
        output_frame.grid_rowconfigure(1, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)
        
        # Output buttons
        button_frame = ttk.Frame(output_frame)
        button_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        
        self.open_csv_btn = ttk.Button(button_frame, text="Open CSV", 
                                      style='Pastel.TButton', command=self.open_csv_file,
                                      state='disabled')
        self.open_csv_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.open_sqlite_btn = ttk.Button(button_frame, text="Open SQLite", 
                                         style='Pastel.TButton', command=self.open_sqlite_file,
                                         state='disabled')
        self.open_sqlite_btn.grid(row=0, column=1, padx=5)
        
        self.clear_log_btn = ttk.Button(button_frame, text="Clear Log", 
                                       style='Pastel.TButton', command=self.clear_log)
        self.clear_log_btn.grid(row=0, column=2, padx=(5, 0))
        
        # Log output
        self.log_text = scrolledtext.ScrolledText(output_frame, height=20, width=50,
                                                 font=('SF Mono', 9), wrap=tk.WORD)
        self.log_text.grid(row=1, column=0, sticky='nsew')
        
        # Configure text tags for colored output
        self.log_text.tag_configure("INFO", foreground=self.colors['text_primary'])
        self.log_text.tag_configure("DEBUG", foreground=self.colors['text_secondary'])
        self.log_text.tag_configure("WARNING", foreground=self.colors['warning'])
        self.log_text.tag_configure("ERROR", foreground=self.colors['error'])
        self.log_text.tag_configure("SUCCESS", foreground=self.colors['success'])
        
    def create_footer(self, parent):
        """Create the footer section."""
        footer_frame = ttk.Frame(parent, style='Card.TFrame')
        footer_frame.grid(row=2, column=0, sticky='ew', pady=(10, 0))
        footer_frame.grid_columnconfigure(0, weight=1)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to scrape!")
        status_label = ttk.Label(footer_frame, textvariable=self.status_var,
                                style='Subtitle.TLabel')
        status_label.grid(row=0, column=0, pady=5)
        
        # Links
        links_frame = ttk.Frame(footer_frame)
        links_frame.grid(row=1, column=0, pady=5)
        
        ttk.Label(links_frame, text="Target Website:", 
                 style='Subtitle.TLabel').grid(row=0, column=0, padx=(0, 5))
        
        website_btn = ttk.Button(links_frame, text="Books to Scrape", 
                                command=lambda: webbrowser.open("https://books.toscrape.com"))
        website_btn.grid(row=0, column=1, padx=5)
        
    def browse_csv_file(self):
        """Browse for CSV output file."""
        filename = filedialog.asksaveasfilename(
            title="Save CSV File",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.csv_filename_var.set(filename)
            
    def browse_sqlite_file(self):
        """Browse for SQLite output file."""
        filename = filedialog.asksaveasfilename(
            title="Save SQLite Database",
            defaultextension=".db",
            filetypes=[("SQLite files", "*.db"), ("All files", "*.*")]
        )
        if filename:
            self.sqlite_filename_var.set(filename)
            
    def log_message(self, message, level="INFO"):
        """Add a message to the log output."""
        self.log_text.insert(tk.END, f"{message}\n", level)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_log(self):
        """Clear the log output."""
        self.log_text.delete(1.0, tk.END)
        
    def update_progress(self, value):
        """Update the progress bar."""
        self.progress_var.set(value)
        self.root.update_idletasks()
        
    def update_status(self, message):
        """Update the status message."""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def start_scraping(self):
        """Start the scraping process in a separate thread."""
        if self.is_running:
            return
            
        # Validate inputs
        try:
            max_pages = int(self.max_pages_var.get())
            delay = float(self.delay_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for pages and delay.")
            return
            
        if not self.csv_var.get() and not self.sqlite_var.get():
            messagebox.showerror("No Output", "Please select at least one output format.")
            return
            
        # Update UI state
        self.is_running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.update_status("Scraping in progress...")
        self.update_progress(0)
        
        # Start scraping in separate thread
        thread = threading.Thread(target=self.run_scraping, 
                                 args=(max_pages, delay), daemon=True)
        thread.start()
        
    def run_scraping(self, max_pages, delay):
        """Run the actual scraping process."""
        try:
            # Initialize scraper
            self.log_message("Initializing scraper...", "INFO")
            self.scraper = BooksToScrapeScraper(delay=delay, log_level=self.log_level_var.get())
            
            # Override the scraper's logger to use our GUI
            original_logger = self.scraper.logger
            self.scraper.logger = type('GUILogger', (), {
                'info': lambda msg: self.log_message(f"INFO: {msg}", "INFO"),
                'warning': lambda msg: self.log_message(f"WARNING: {msg}", "WARNING"),
                'error': lambda msg: self.log_message(f"ERROR: {msg}", "ERROR"),
                'debug': lambda msg: self.log_message(f"DEBUG: {msg}", "DEBUG")
            })()
            
            # Scrape books
            self.log_message(f"Starting to scrape {max_pages} pages...", "INFO")
            books = self.scraper.scrape_books(max_pages=max_pages, deep=self.deep_var.get())
            
            if not books:
                self.log_message("No books were scraped!", "ERROR")
                return
                
            # Update progress
            self.update_progress(50)
            
            # Save to files
            if self.csv_var.get():
                csv_file = self.csv_filename_var.get()
                self.log_message(f"Saving to CSV: {csv_file}", "INFO")
                self.scraper.save_to_csv(books, csv_file)
                self.open_csv_btn.config(state='normal')
                
            if self.sqlite_var.get():
                sqlite_file = self.sqlite_filename_var.get()
                self.log_message(f"Saving to SQLite: {sqlite_file}", "INFO")
                self.scraper.save_to_sqlite(books, sqlite_file)
                self.open_sqlite_btn.config(state='normal')
                
            # Update progress
            self.update_progress(100)
            
            # Show completion message
            self.log_message(f"Scraping completed successfully!", "SUCCESS")
            self.log_message(f"Total books scraped: {len(books)}", "SUCCESS")
            self.update_status(f"Completed! Scraped {len(books)} books")
            
            # Show sample data
            self.log_message("\n" + "="*50, "INFO")
            self.log_message("SAMPLE DATA - First 5 books:", "INFO")
            self.log_message("="*50, "INFO")
            
            for i, book in enumerate(books[:5]):
                self.log_message(f"{i+1}. {book.title[:50]}... | {book.price} | Rating: {book.rating}", "INFO")
                
        except Exception as e:
            self.log_message(f"Error during scraping: {str(e)}", "ERROR")
            self.update_status("Scraping failed!")
            
        finally:
            # Reset UI state
            self.is_running = False
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.update_progress(0)
            
    def stop_scraping(self):
        """Stop the scraping process."""
        self.is_running = False
        self.log_message("Scraping stopped by user", "WARNING")
        self.update_status("Scraping stopped")
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        
    def open_csv_file(self):
        """Open the CSV file in the default application."""
        csv_file = self.csv_filename_var.get()
        if os.path.exists(csv_file):
            os.system(f"open '{csv_file}'")
        else:
            messagebox.showerror("File Not Found", f"CSV file not found: {csv_file}")
            
    def open_sqlite_file(self):
        """Open the SQLite file location."""
        sqlite_file = self.sqlite_filename_var.get()
        if os.path.exists(sqlite_file):
            os.system(f"open '{os.path.dirname(sqlite_file)}'")
        else:
            messagebox.showerror("File Not Found", f"SQLite file not found: {sqlite_file}")


def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    app = ScraperGUI(root)
    
    # Handle window closing
    def on_closing():
        if app.is_running:
            if messagebox.askokcancel("Quit", "Scraping is in progress. Do you want to quit?"):
                app.stop_scraping()
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()

