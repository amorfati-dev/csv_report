"""KPI calculation module for CSV analysis.

This module provides comprehensive KPI calculation functions for analyzing
CSV data, particularly focused on S&P 500 companies data.
"""

from typing import Any, Dict

import pandas as pd

__all__ = [
    "calculate_base_kpis",
    "calculate_enhanced_kpis",
    "calculate_sector_kpis",
    "compute_all_kpis",
    "compute_kpis",
]


def compute_kpis(df: pd.DataFrame) -> dict:
    """Basic KPI calculation for quick analysis (legacy function)."""
    numeric = df.select_dtypes("number")
    return {
        "rows": len(df),
        "cols": len(df.columns),
        "means": numeric.mean().round(2).to_dict(),
    }


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
        "avg_market_cap": float(df["Marketcap"].mean()),
        "median_market_cap": float(df["Marketcap"].median()),
    }


def calculate_sector_kpis(df: pd.DataFrame) -> dict[str, Any]:
    """Calculate KPIs for each sector.

    Args:
        df: DataFrame containing S&P 500 companies data

    Returns:
        Dictionary with sector statistics containing:
        - sectors: List of sector data with avg_market_cap, median_market_cap,
        company_count

    """
    sector_stats = df.groupby("Sector").agg({"Marketcap": ["mean", "median", "count"]})

    # Flatten column names
    sector_stats.columns = ["avg_market_cap", "median_market_cap", "company_count"]

    sector_stats = sector_stats.reset_index()

    # Convert to list of dictionaries for JSON serialization
    sectors = []
    for _, row in sector_stats.iterrows():
        sectors.append(
            {
                "sector": str(row["Sector"]),
                "avg_market_cap": float(row["avg_market_cap"]),
                "median_market_cap": float(row["median_market_cap"]),
                "company_count": int(row["company_count"]),
            },
        )

    return {"sectors": sectors}


def calculate_enhanced_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate enhanced KPIs including top companies, market cap distribution, and
    percentiles.

    Args:
        df: DataFrame containing S&P 500 companies data

    Returns:
        Dictionary containing comprehensive analysis

    """
    # Top 10 companies by market cap
    top_companies_df = df.nlargest(10, "Marketcap")[
        ["Symbol", "Shortname", "Marketcap", "Sector"]
    ].copy()
    top_companies_df["Marketcap_B"] = (
        top_companies_df["Marketcap"] / 1e9
    )  # Convert to billions

    # Convert to list of dictionaries for JSON serialization
    top_companies = []
    for _, row in top_companies_df.iterrows():
        top_companies.append(
            {
                "symbol": str(row["Symbol"]),
                "shortname": str(row["Shortname"]),
                "marketcap": float(row["Marketcap"]),
                "marketcap_b": float(row["Marketcap_B"]),
                "sector": str(row["Sector"]),
            },
        )

    # Market cap percentiles
    percentiles_raw = df["Marketcap"].quantile([0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
    percentiles = {f"p{int(k*100)}": float(v) for k, v in percentiles_raw.items()}

    # Market cap distribution (Small: <$2B, Mid: $2B-$10B, Large: >$10B)
    small_cap = df[df["Marketcap"] < 2e9]
    mid_cap = df[(df["Marketcap"] >= 2e9) & (df["Marketcap"] < 10e9)]
    large_cap = df[df["Marketcap"] >= 10e9]
    mega_cap = df[df["Marketcap"] >= 100e9]  # $100B+

    # Sector rankings
    sector_rankings_df = (
        df.groupby("Sector")
        .agg({"Marketcap": ["mean", "median", "count", "sum"]})
        .round(2)
    )
    sector_rankings_df.columns = [
        "avg_market_cap",
        "median_market_cap",
        "company_count",
        "total_market_cap",
    ]
    sector_rankings_df = sector_rankings_df.sort_values(
        "avg_market_cap",
        ascending=False,
    ).reset_index()

    # Convert to list of dictionaries for JSON serialization
    sector_rankings = []
    for _, row in sector_rankings_df.iterrows():
        sector_rankings.append(
            {
                "sector": str(row["Sector"]),
                "avg_market_cap": float(row["avg_market_cap"]),
                "median_market_cap": float(row["median_market_cap"]),
                "company_count": int(row["company_count"]),
                "total_market_cap": float(row["total_market_cap"]),
            },
        )

    # Technology vs Traditional sectors
    tech_sectors = ["Technology", "Communication Services"]
    tech_companies = df[df["Sector"].isin(tech_sectors)]
    traditional_companies = df[~df["Sector"].isin(tech_sectors)]

    # Sector concentration (top 5 sectors by market cap)
    top_sectors_by_market_cap_df = sector_rankings_df.nlargest(5, "total_market_cap")
    top_sectors_by_market_cap = []
    for _, row in top_sectors_by_market_cap_df.iterrows():
        top_sectors_by_market_cap.append(
            {
                "sector": str(row["Sector"]),
                "avg_market_cap": float(row["avg_market_cap"]),
                "median_market_cap": float(row["median_market_cap"]),
                "company_count": int(row["company_count"]),
                "total_market_cap": float(row["total_market_cap"]),
            },
        )

    return {
        "top_companies": top_companies,
        "percentiles": percentiles,
        "market_cap_distribution": {
            "small_cap_count": len(small_cap),
            "mid_cap_count": len(mid_cap),
            "large_cap_count": len(large_cap),
            "mega_cap_count": len(mega_cap),
            "small_cap_pct": float(len(small_cap) / len(df) * 100),
            "mid_cap_pct": float(len(mid_cap) / len(df) * 100),
            "large_cap_pct": float(len(large_cap) / len(df) * 100),
            "mega_cap_pct": float(len(mega_cap) / len(df) * 100),
        },
        "sector_rankings": sector_rankings,
        "tech_vs_traditional": {
            "tech_companies": len(tech_companies),
            "traditional_companies": len(traditional_companies),
            "tech_market_cap": float(tech_companies["Marketcap"].sum()),
            "traditional_market_cap": float(traditional_companies["Marketcap"].sum()),
            "tech_avg_market_cap": float(tech_companies["Marketcap"].mean()),
            "traditional_avg_market_cap": float(
                traditional_companies["Marketcap"].mean(),
            ),
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
