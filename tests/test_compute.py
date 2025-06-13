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
    assert kpis['avg_market_cap'] == 1766666666666.6667
    assert kpis['median_market_cap'] == 1800000000000


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
    assert len(kpis) == 1  # Only one sector
    assert kpis['Sector'].iloc[0] == 'Technology'
    assert kpis['avg_market_cap'].iloc[0] == 1766666666666.6667
    assert kpis['median_market_cap'].iloc[0] == 1800000000000
    assert kpis['company_count'].iloc[0] == 3 