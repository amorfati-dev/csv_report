"""Tests for the KPI computation module."""

import pandas as pd

from kpi_service.kpi import calculate_base_kpis, calculate_sector_kpis


def test_calculate_base_kpis() -> None:
    """Test calculation of base KPIs."""
    # Create sample data
    data = {
        "Symbol": ["AAPL", "MSFT", "GOOGL"],
        "Shortname": ["Apple", "Microsoft", "Alphabet"],
        "Marketcap": [2000000000000, 1800000000000, 1500000000000],
        "Sector": ["Technology", "Technology", "Technology"],
    }
    df = pd.DataFrame(data)

    # Calculate KPIs
    kpis = calculate_base_kpis(df)

    # Check results
    assert kpis["total_companies"] == 3
    assert kpis["avg_market_cap"] == 1766666666666.6667
    assert kpis["median_market_cap"] == 1800000000000


def test_calculate_sector_kpis() -> None:
    """Test calculation of sector KPIs."""
    # Create sample data
    data = {
        "Symbol": ["AAPL", "MSFT", "GOOGL"],
        "Shortname": ["Apple", "Microsoft", "Alphabet"],
        "Marketcap": [2000000000000, 1800000000000, 1500000000000],
        "Sector": ["Technology", "Technology", "Technology"],
    }
    df = pd.DataFrame(data)

    # Calculate KPIs
    kpis = calculate_sector_kpis(df)

    # Check results
    assert "sectors" in kpis
    assert len(kpis["sectors"]) == 1  # Only one sector
    sector_data = kpis["sectors"][0]
    assert sector_data["sector"] == "Technology"
    assert sector_data["avg_market_cap"] == 1766666666666.6667
    assert sector_data["median_market_cap"] == 1800000000000
    assert sector_data["company_count"] == 3
