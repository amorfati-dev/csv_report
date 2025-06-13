import pytest
from pathlib import Path
import pandas as pd
from csv_report.report.generate import generate_report, save_report

def test_generate_report():
    """Test report generation from DataFrame."""
    # Create sample data
    data = {
        'Symbol': ['AAPL', 'MSFT', 'GOOGL'],
        'Shortname': ['Apple', 'Microsoft', 'Alphabet'],
        'Marketcap': [2000000000000, 1800000000000, 1500000000000],
        'Sector': ['Technology', 'Technology', 'Technology']
    }
    df = pd.DataFrame(data)
    
    # Generate report
    report = generate_report(df)
    
    # Check report content
    assert isinstance(report, str)
    assert "S&P 500 Analysis Report" in report
    assert "Apple" in report
    assert "Microsoft" in report
    assert "Alphabet" in report

def test_save_report(tmp_path):
    """Test saving report to file."""
    # Create sample report content
    report_content = "Test Report Content"
    
    # Save report
    report_path = tmp_path / "test_report.md"
    saved_path = save_report(report_content, report_path)
    
    assert saved_path == report_path
    assert report_path.exists()
    assert report_path.read_text() == "Test Report Content"

def test_generate_report_empty_data():
    """Test report generation with empty DataFrame."""
    df = pd.DataFrame(columns=['Symbol', 'Shortname', 'Marketcap', 'Sector'])
    
    # Generate report
    report = generate_report(df)
    
    # Check report content
    assert isinstance(report, str)
    assert "No data available for analysis" in report 