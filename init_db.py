#!/usr/bin/env python3
"""Standalone script to initialize the CSV report database."""

import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from csv_report.db_init import main

if __name__ == "__main__":
    main() 