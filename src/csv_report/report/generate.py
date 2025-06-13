"""Generate reports from S&P 500 companies data.

This module provides functions to generate and save reports from the
S&P 500 companies data.
"""
from __future__ import annotations

import pandas as pd
from pathlib import Path
from typing import Optional

__all__ = ["generate_report", "save_report"]


def generate_report(df: pd.DataFrame) -> str:
    """Generate a report from the S&P 500 companies data.
    
    Args:
        df: DataFrame containing S&P 500 companies data
        
    Returns:
        String containing the formatted report
    """
    if df.empty:
        return "No data available for analysis."
    
    # Get company names
    companies = df["Shortname"].tolist()
    
    # Generate report
    report = [
        "S&P 500 Analysis Report",
        "=" * 20,
        "",
        "Companies Analyzed:",
        *[f"- {company}" for company in companies],
        "",
        "End of Report"
    ]
    
    return "\n".join(report)


def save_report(report: str, output_file: Optional[Path] = None) -> Path:
    """Save a report to a file.
    
    Args:
        report: The report content to save
        output_file: Optional path to save the report (defaults to report.txt)
        
    Returns:
        Path to the saved report file
    """
    if output_file is None:
        output_file = Path("report.txt")
    
    output_file.write_text(report)
    return output_file