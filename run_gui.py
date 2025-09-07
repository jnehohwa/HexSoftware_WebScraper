#!/usr/bin/env python3
"""
Quick launcher for the HexSoftwares Web Scraper GUI
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from scraper_gui import main
    main()
except ImportError as e:
    print(f"Error importing GUI: {e}")
    print("Make sure you have installed the requirements:")
    print("pip install -r requirements.txt")
    sys.exit(1)

