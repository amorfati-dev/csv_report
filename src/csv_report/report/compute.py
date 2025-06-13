"""Compute various KPIs from the S&P 500 companies DataFrame.

This module provides functions to calculate key performance indicators
and statistics from the S&P 500 companies data.
"""

from __future__ import annotations

import pandas as pd
from typing import Dict, Any
from ..load import load_csv

__all__ = ["calculate_base_kpis", "calculate_sector_kpis"]


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
