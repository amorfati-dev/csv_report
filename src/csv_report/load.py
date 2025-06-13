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
import os
import requests
from io import StringIO

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
    """Get the default path to the CSV file.

    Returns:
        Path to the default CSV file
    """
    return Path(__file__).parent.parent.parent / "data" / "sp500.csv"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def load_csv(
    file_path: Optional[Union[str, Path]] = None,
    url: Optional[str] = None
) -> pd.DataFrame:
    """Load CSV data from a file or URL.

    Args:
        file_path: Path to the CSV file. If None, uses the default path.
        url: URL to download the CSV from. If provided, overrides file_path.

    Returns:
        DataFrame containing the CSV data

    Raises:
        FileNotFoundError: If the file doesn't exist and no URL is provided
        ValueError: If neither file_path nor url is provided
    """
    if url:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return pd.read_csv(StringIO(response.text))
        except requests.RequestException as e:
            raise ValueError(f"Failed to download CSV from URL: {e}")

    if file_path is None:
        file_path = get_default_csv_path()

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"CSV file not found at {file_path}. "
            "Please provide a valid file path or URL."
        )

    return pd.read_csv(file_path)
