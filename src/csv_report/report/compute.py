"""Compute various KPIs from the S&P 500 companies DataFrame.

This module provides functions to calculate key performance indicators
and statistics from the S&P 500 companies data.
"""

from __future__ import annotations

import pandas as pd
from typing import Dict, Any
from ..load import load_csv

__all__ = ["calculate_base_kpis", "calculate_sector_kpis", "calculate_enhanced_kpis"]


def calculate_base_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate base KPIs for the entire dataset.

    Args:
        df: DataFrame containing S&P 500 companies data

    Returns:
        Dictionary containing:
        - total_companies: Number of companies
        - avg_market_cap: Average market capitalization
        - median_market_cap: Median market capitalization
    """
    return {
        "total_companies": len(df),
        "avg_market_cap": df["Marketcap"].mean(),
        "median_market_cap": df["Marketcap"].median(),
    }


def calculate_sector_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate KPIs for each sector.

    Args:
        df: DataFrame containing S&P 500 companies data

    Returns:
        DataFrame with sector statistics containing:
        - avg_market_cap: Average market cap per sector
        - median_market_cap: Median market cap per sector
        - company_count: Number of companies per sector
    """
    sector_stats = df.groupby("Sector").agg({"Marketcap": ["mean", "median", "count"]})

    # Flatten column names
    sector_stats.columns = ["avg_market_cap", "median_market_cap", "company_count"]

    return sector_stats.reset_index()


def calculate_enhanced_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate enhanced KPIs including top companies, market cap distribution, and percentiles.

    Args:
        df: DataFrame containing S&P 500 companies data

    Returns:
        Dictionary containing comprehensive analysis
    """
    # Top 10 companies by market cap
    top_companies = df.nlargest(10, 'Marketcap')[['Symbol', 'Shortname', 'Marketcap', 'Sector']].copy()
    top_companies['Marketcap_B'] = top_companies['Marketcap'] / 1e9  # Convert to billions
    
    # Market cap percentiles
    percentiles = df['Marketcap'].quantile([0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
    
    # Market cap distribution (Small: <$2B, Mid: $2B-$10B, Large: >$10B)
    small_cap = df[df['Marketcap'] < 2e9]
    mid_cap = df[(df['Marketcap'] >= 2e9) & (df['Marketcap'] < 10e9)]
    large_cap = df[df['Marketcap'] >= 10e9]
    mega_cap = df[df['Marketcap'] >= 100e9]  # $100B+
    
    # Sector rankings
    sector_rankings = df.groupby('Sector').agg({
        'Marketcap': ['mean', 'median', 'count', 'sum']
    }).round(2)
    sector_rankings.columns = ['avg_market_cap', 'median_market_cap', 'company_count', 'total_market_cap']
    sector_rankings = sector_rankings.sort_values('avg_market_cap', ascending=False).reset_index()
    
    # Technology vs Traditional sectors
    tech_sectors = ['Technology', 'Communication Services']
    tech_companies = df[df['Sector'].isin(tech_sectors)]
    traditional_companies = df[~df['Sector'].isin(tech_sectors)]
    
    # Sector concentration (top 5 sectors by market cap)
    top_sectors_by_market_cap = sector_rankings.nlargest(5, 'total_market_cap')
    
    return {
        "top_companies": top_companies,
        "percentiles": percentiles,
        "market_cap_distribution": {
            "small_cap_count": len(small_cap),
            "mid_cap_count": len(mid_cap),
            "large_cap_count": len(large_cap),
            "mega_cap_count": len(mega_cap),
            "small_cap_pct": len(small_cap) / len(df) * 100,
            "mid_cap_pct": len(mid_cap) / len(df) * 100,
            "large_cap_pct": len(large_cap) / len(df) * 100,
            "mega_cap_pct": len(mega_cap) / len(df) * 100,
        },
        "sector_rankings": sector_rankings,
        "tech_vs_traditional": {
            "tech_companies": len(tech_companies),
            "traditional_companies": len(traditional_companies),
            "tech_market_cap": tech_companies['Marketcap'].sum(),
            "traditional_market_cap": traditional_companies['Marketcap'].sum(),
            "tech_avg_market_cap": tech_companies['Marketcap'].mean(),
            "traditional_avg_market_cap": traditional_companies['Marketcap'].mean(),
        },
        "top_sectors_by_market_cap": top_sectors_by_market_cap,
    }


def compute_all_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute all KPIs and return them in a structured format.

    Args:
        df: DataFrame containing S&P 500 companies data

    Returns:
        Dictionary containing both base KPIs and sector KPIs
    """
    return {
        "base_kpis": calculate_base_kpis(df),
        "sector_kpis": calculate_sector_kpis(df),
        "enhanced_kpis": calculate_enhanced_kpis(df),
    }


def test_compute():
    """Test function to run the compute functions and print results."""
    # Load the data
    df = load_csv()

    # Calculate all KPIs
    kpis = compute_all_kpis(df)

    # Print base KPIs
    print("\n=== Base KPIs ===")
    print(f"Total Companies: {kpis['base_kpis']['total_companies']}")
    print(f"Average Market Cap: ${kpis['base_kpis']['avg_market_cap']:,.2f}")
    print(f"Median Market Cap: ${kpis['base_kpis']['median_market_cap']:,.2f}")

    # Print sector KPIs
    print("\n=== Sector KPIs ===")
    pd.set_option("display.float_format", lambda x: "${:,.2f}".format(x))
    print(kpis["sector_kpis"].to_string(index=False))


if __name__ == "__main__":
    test_compute()
