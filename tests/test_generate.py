"""Tests for the generate module."""

import pandas as pd
import tempfile
from pathlib import Path
from csv_report.report.generate import generate_report, save_report

def test_generate_report():
    """Test report generation."""
    # Create sample data
    data = {
        "Symbol": ["AAPL", "MSFT", "GOOGL"],
        "Shortname": ["Apple", "Microsoft", "Alphabet"],
        "Marketcap": [2000000000000, 1800000000000, 1500000000000],
        "Sector": ["Technology", "Technology", "Technology"],
    }
    df = pd.DataFrame(data)


    # Generate report
    report = generate_report(df)

    # Check report content - updated to match new template
    assert "📊 S&P 500 Companies Analysis Report" in report
    assert "Apple" in report
    assert "Microsoft" in report
    assert "Alphabet" in report


def test_save_report():
    """Test saving report to file."""
    # Create test report
    report = "Test Report\n==========\n\nTest content."

    # Create temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.markdown', delete=False) as tmp:
        tmp_path = Path(tmp.name)

    # Save report to temporary file
    output_file = save_report(report, output_file=tmp_path)

    # Check file exists and content
    assert output_file.exists()
    assert output_file.read_text() == report

    # Clean up temporary file
    output_file.unlink()


def test_generate_report_empty_data():
    """Test report generation with empty data."""
    # Create empty DataFrame
    df = pd.DataFrame()

    # Generate report
    report = generate_report(df)

    # Check report content
    assert report == "No data available for analysis."
