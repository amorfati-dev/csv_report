"""Tests for the compute module."""
import pandas as pd
from csv_report.report.compute import calculate_base_kpis, calculate_sector_kpis


def test_calculate_base_kpis():
    """Test calculation of base KPIs."""
    # Create sample data
    data = {
        'Symbol': ['AAPL', 'MSFT', 'GOOGL'],
        'Shortname': ['Apple', 'Microsoft', 'Alphabet'],
        'Marketcap': [2000000000000, 1800000000000, 1500000000000],
        'Sector': ['Technology', 'Technology', 'Technology']
    }
    df = pd.DataFrame(data)

    # Calculate KPIs
    kpis = calculate_base_kpis(df)

    # Check results
    assert kpis['total_companies'] == 3
    assert kpis['total_marketcap'] == 5300000000000
    assert kpis['avg_marketcap'] == 1766666666666.67


def test_calculate_sector_kpis():
    """Test calculation of sector KPIs."""
    # Create sample data
    data = {
        'Symbol': ['AAPL', 'MSFT', 'GOOGL'],
        'Shortname': ['Apple', 'Microsoft', 'Alphabet'],
        'Marketcap': [2000000000000, 1800000000000, 1500000000000],
        'Sector': ['Technology', 'Technology', 'Technology']
    }
    df = pd.DataFrame(data)

    # Calculate KPIs
    kpis = calculate_sector_kpis(df)

    # Check results
    assert 'Technology' in kpis
    assert kpis['Technology']['count'] == 3
    assert kpis['Technology']['total_marketcap'] == 5300000000000 