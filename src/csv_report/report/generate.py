"""Generate reports from S&P 500 companies data using Jinja2 templates.

This module provides functions to generate and save reports from the
S&P 500 companies data using Jinja2 templates.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import Environment, FileSystemLoader

# Add kpi_service to path and import
sys.path.append(str(Path(__file__).parent.parent.parent))
from kpi_service.kpi import calculate_base_kpis, calculate_enhanced_kpis

if TYPE_CHECKING:
    import pandas as pd

__all__ = ["generate_report", "save_report"]


def generate_report(df: pd.DataFrame, output_format: str = "markdown") -> str:
    """Generate a report from the S&P 500 companies data using Jinja2 template.

    Args:
        df: DataFrame containing S&P 500 companies data
        output_format: 'html' or 'markdown'

    Returns:
        String containing the formatted report

    """
    if df.empty:
        return "No data available for analysis."

    # Compute KPIs
    base_kpis = calculate_base_kpis(df)
    enhanced_kpis = calculate_enhanced_kpis(df)

    # Legacy sector KPIs for backward compatibility
    sector_kpis = (
        df.groupby("Sector")
        .agg({"Shortname": "count", "Marketcap": ["mean", "median"]})
        .round(2)
    )

    # Flatten column names
    sector_kpis.columns = ["company_count", "avg_market_cap", "median_market_cap"]
    sector_kpis = sector_kpis.reset_index()

    # Load Jinja2 template
    template_dir = Path(__file__).parent
    env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
    if output_format == "html":
        template = env.get_template("report_template.html")
    else:
        template = env.get_template("template.markdown.j2")

    # Render template with data
    return template.render(
        base_kpis=base_kpis,
        sector_kpis=sector_kpis,
        enhanced_kpis=enhanced_kpis,
        generated_at=datetime.now().strftime("%B %d, %Y at %I:%M:%S %p"),
    )


def save_report(report: str, output_file: Path | None = None) -> Path:
    """Save a report to a file.

    Args:
        report: The report content to save
        output_file: Optional path to save the report (defaults to
        sp500_analysis.markdown)

    Returns:
        Path to the saved report file

    """
    if output_file is None:
        output_file = Path("reports/sp500_analysis.markdown")

    # Ensure reports directory exists
    output_file.parent.mkdir(exist_ok=True)

    output_file.write_text(report)
    return output_file
