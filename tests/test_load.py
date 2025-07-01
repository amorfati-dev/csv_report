"""Tests for the load module."""

import pandas as pd
import pytest

from csv_report.load import load_csv


def test_load_default_csv() -> None:
    """Test loading default CSV file."""
    # Create sample data
    data = {
        "Symbol": ["AAPL", "MSFT", "GOOGL"],
        "Shortname": ["Apple", "Microsoft", "Alphabet"],
        "Marketcap": [2000000000000, 1800000000000, 1500000000000],
        "Sector": ["Technology", "Technology", "Technology"],
    }
    df = pd.DataFrame(data)

    # Save to default location
    df.to_csv("data/sp500.csv", index=False)

    # Load data
    loaded_df = load_csv()

    # Check data
    assert isinstance(loaded_df, pd.DataFrame)
    assert len(loaded_df) == 3
    assert "Apple" in loaded_df["Shortname"].values


def test_load_csv_from_url() -> None:
    """Test loading CSV from URL."""
    # Create sample data
    data = {
        "Symbol": ["AAPL", "MSFT", "GOOGL"],
        "Shortname": ["Apple", "Microsoft", "Alphabet"],
        "Marketcap": [2000000000000, 1800000000000, 1500000000000],
        "Sector": ["Technology", "Technology", "Technology"],
    }
    df = pd.DataFrame(data)

    # Save to temporary file
    df.to_csv("data/sp500.csv", index=False)

    # Load data
    loaded_df = load_csv(csv_file="data/sp500.csv")

    # Check data
    assert isinstance(loaded_df, pd.DataFrame)
    assert len(loaded_df) == 3
    assert "Apple" in loaded_df["Shortname"].values


def test_load_invalid_file() -> None:
    """Test loading invalid file."""
    with pytest.raises(FileNotFoundError):
        load_csv("nonexistent.csv")
