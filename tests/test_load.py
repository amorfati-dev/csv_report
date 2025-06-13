import pytest
from pathlib import Path
import pandas as pd
from csv_report.load import load_csv, DataLoadError, get_default_csv_path

def test_load_default_csv():
    """Test loading the default S&P 500 CSV file."""
    # Load the default CSV file
    df = load_csv()
    
    # Check that we got a DataFrame
    assert isinstance(df, pd.DataFrame)
    
    # Check required columns are present
    required_columns = ['Symbol', 'Shortname', 'Marketcap', 'Sector']
    for col in required_columns:
        assert col in df.columns
    
    # Check we have some data
    assert len(df) > 0

def test_load_csv_from_url():
    """Test loading a CSV file from a URL."""
    # Use a sample CSV URL (S&P 500 constituents from datasets)
    test_url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
    
    # Load the CSV from URL with the expected columns for this file
    df = load_csv(test_url, required_columns=['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry'])
    
    # Check that we got a DataFrame
    assert isinstance(df, pd.DataFrame)
    
    # Check for expected columns in the S&P 500 dataset from this URL
    expected_columns = ['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry']
    for col in expected_columns:
        assert col in df.columns
    
    # Check we have some data
    assert len(df) > 0

def test_load_invalid_file():
    """Test error handling for invalid files."""
    # Try to load a non-existent file
    with pytest.raises(DataLoadError) as exc_info:
        load_csv("nonexistent_file.csv")
    
    # Check the error message
    assert "CSV file not found" in str(exc_info.value)
    
    # Try to load a file with missing required columns
    # Create a temporary CSV with wrong columns
    temp_file = Path("temp_test.csv")
    pd.DataFrame({'Wrong': ['Column']}).to_csv(temp_file, index=False)
    
    try:
        with pytest.raises(DataLoadError) as exc_info:
            load_csv(temp_file)
        assert "Missing required columns" in str(exc_info.value)
    finally:
        # Clean up the temporary file
        if temp_file.exists():
            temp_file.unlink() 