# csv_report/load.py
"""Load S&P 500 companies data from CSV file or URL.

This module provides functions to load S&P 500 companies data from either
a local CSV file or a remote URL.
"""

from __future__ import annotations

from io import StringIO
from pathlib import Path

import pandas as pd

# Optional import for URL functionality
try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

__all__ = ["load_csv"]


def load_csv(
    csv_file: str | Path | None = None,
    url: str | None = None,
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
    if url is not None:
        if not REQUESTS_AVAILABLE:
            msg = (
                "requests library is required for URL loading. "
                "Install with: pip install requests"
            )
            raise ImportError(
                msg,
            )
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return pd.read_csv(StringIO(response.text))
    # Try to load from default location
    default_file = Path("data/sp500.csv")
    if default_file.exists():
        return pd.read_csv(default_file)
    msg = "No CSV file or URL provided, and default file not found"
    raise ValueError(msg)
