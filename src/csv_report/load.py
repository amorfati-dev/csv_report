# csv_report/load.py
"""Light‑weight utilities for loading CSV data.

This module abstracts *where* the CSV comes from (local path vs. HTTP(S)
URL) and returns a **pandas.DataFrame** ready for further processing.
All potentially fragile I/O is concentrated here so that the rest of the
project can focus on analysis and reporting.
"""
from __future__ import annotations

import tempfile
import urllib.request
from pathlib import Path
from typing import Union, Optional
from urllib.parse import urlparse
from typing import Optional, Union

import pandas as pd

__all__ = ["DataLoadError", "load_csv"]


class DataLoadError(Exception):
    """Raised when a CSV file cannot be loaded or parsed."""

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _is_url(s: str) -> bool:
    """Return *True* if *s* looks like an HTTP(S) URL."""
    try:
        parsed = urlparse(s)
        return parsed.scheme in {"http", "https"}
    except Exception:
        return False


def _download_to_tmp(url: str) -> Path:
    """Download the given *url* to a temporary file and return its path."""
    tmp_path = Path(tempfile.mkstemp(suffix=".csv")[1])  # secure temp file
    try:
        urllib.request.urlretrieve(url, tmp_path)
    except Exception as exc:
        raise DataLoadError(f"Download failed for URL: {url}") from exc
    return tmp_path


def get_default_csv_path() -> Path:
    """Get the default path to the S&P 500 companies CSV file."""
    # Go up from src/csv_report to project root
    project_root = Path(__file__).parent.parent.parent
    return project_root / 'data' / 'sp500_companies.csv'


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def load_csv(source: Optional[str | Path] = None, required_columns: Optional[list[str]] = None) -> pd.DataFrame:
    """Load CSV data from a file or URL.
    
    Args:
        source: Path to CSV file or URL. If None, uses default S&P 500 file.
        required_columns: List of columns to require. If None, use default. If empty list, skip check.
        
    Returns:
        DataFrame containing the CSV data.
        
    Raises:
        DataLoadError: If the file cannot be loaded or parsed.
    """
    try:
        # Use default path if no source provided
        if source is None:
            source = get_default_csv_path()
            
        # Convert string to Path if needed
        if _is_url(source):
            source = _download_to_tmp(source)
        else:
            source = Path(source)
            
        # Check if file exists
        if not source.exists():
            raise DataLoadError(f"CSV file not found: {source}")
            
        # Load the data
        df = pd.read_csv(source)
        
        # Validate required columns
        if required_columns is None:
            required_columns_check = ['Symbol', 'Shortname', 'Marketcap', 'Sector']
        else:
            required_columns_check = required_columns
        if required_columns_check:
            missing_columns = [col for col in required_columns_check if col not in df.columns]
            if missing_columns:
                raise DataLoadError(f"Missing required columns: {', '.join(missing_columns)}")
        
        return df
        
    except pd.errors.ParserError as e:
        raise DataLoadError(f"Could not parse CSV file: {e}")
    except Exception as e:
        raise DataLoadError(f"Error loading CSV file: {e}")
