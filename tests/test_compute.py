"""Tests for the compute module."""
import pytest
import pandas as pd
from csv_report.report.compute import calculate_base_kpis, calculate_sector_kpis

def test_calculate_base_kpis():
    """Test base KPI calculations."""
    # Create sample data
    data = {
        'Marketcap': [1000000, 2000000, 3000000],
        'Sector': ['Tech', 'Tech', 'Finance']
    }
    df = pd.DataFrame(data)
    
    # Calculate KPIs
    kpis = calculate_base_kpis(df)
    
    # Check results
    assert kpis['total_companies'] == 3
    assert kpis['avg_market_cap'] == 2000000
    assert kpis['median_market_cap'] == 2000000

def test_calculate_sector_kpis():
    """Test sector KPI calculations."""
    # Create sample data
    data = {
        'Marketcap': [1000000, 2000000, 3000000],
        'Sector': ['Tech', 'Tech', 'Finance']
    }
    df = pd.DataFrame(data)
    
    # Calculate sector KPIs
    sector_kpis = calculate_sector_kpis(df)
    
    # Check results
    assert len(sector_kpis) == 2  # Two sectors
    assert 'Tech' in sector_kpis['Sector'].values
    assert 'Finance' in sector_kpis['Sector'].values
    
    # Check Tech sector
    tech_row = sector_kpis[sector_kpis['Sector'] == 'Tech'].iloc[0]
    assert tech_row['company_count'] == 2
    assert tech_row['avg_market_cap'] == 1500000 