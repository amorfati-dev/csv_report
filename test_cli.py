#!/usr/bin/env python3
"""Test script to demonstrate the new Typer CLI functionality."""

import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from csv_report.main import app

if __name__ == "__main__":
    print("🧪 Testing CSV Report CLI with Typer and database integration...")
    print("\n1. First, let's show any existing runs:")
    app(["show-runs", "--limit", "5"])
    
    print("\n" + "="*60)
    print("2. Now let's generate a report (this will create a run record):")
    # Note: This might fail if no CSV file is available, but it will still create a run record
    try:
        app(["generate", "--output-format", "markdown"])
    except Exception as e:
        print(f"Expected error (no CSV file): {e}")
    
    print("\n" + "="*60)
    print("3. Let's show the runs again to see the new record:")
    app(["show-runs", "--limit", "5"]) 