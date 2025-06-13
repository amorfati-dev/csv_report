"""Tests for the load module."""
import pytest
import pandas as pd
from csv_report.load import load_csv


def test_load_default_csv():
    """Test loading the default CSV file."""
    df = load_csv()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_load_csv_from_url():
    """Test loading CSV from URL."""
    url = (
        "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/"
        "master/data/constituents.csv"
    )
    df = load_csv(url=url)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_load_invalid_file():
    """Test loading non-existent file."""
    with pytest.raises(FileNotFoundError):
        load_csv(file_path="nonexistent.csv") 