#!/usr/bin/env python3
"""Test script to demonstrate the new Typer CLI functionality."""

import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

import contextlib

from csv_report.main import app

if __name__ == "__main__":
    app(["show-runs", "--limit", "5"])

    # Note: This might fail if no CSV file is available, but it will still create a run record
    with contextlib.suppress(Exception):
        app(["generate", "--output-format", "markdown"])

    app(["show-runs", "--limit", "5"])
