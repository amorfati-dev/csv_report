# csv_report/load.py
"""Load S&P 500 companies data from CSV file or URL.

This module provides functions to load S&P 500 companies data from either
a local CSV file or a remote URL.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Union
import pandas as pd
import requests
from io import StringIO

__all__ = ["load_csv"]


def load_csv(
    csv_file: Optional[Union[str, Path]] = None,
    url: Optional[str] = None
) -> pd.DataFrame:
    """Load S&P 500 companies data from CSV file or URL.
    
    Args:
        csv_file: Path to local CSV file (optional)
        url: URL to remote CSV file (optional)
        
    Returns:
        DataFrame containing S&P 500 companies data
        
    Raises:
        FileNotFoundError: If local file not found
        requests.RequestException: If URL request fails
        ValueError: If neither file nor URL provided
    """
    if csv_file is not None:
        return pd.read_csv(csv_file)
    elif url is not None:
        response = requests.get(url)
        response.raise_for_status()
        return pd.read_csv(StringIO(response.text))
    else:
        # Try to load from default location
        default_file = Path("data/sp500.csv")
        if default_file.exists():
            return pd.read_csv(default_file)
        raise ValueError("No CSV file or URL provided, and default file not found")
