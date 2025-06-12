"""Generate reports from computed KPIs using Jinja2 templates."""
from __future__ import annotations

import os
import warnings
from pathlib import Path
from typing import Dict, Any

import jinja2
import pandas as pd
from ..load import load_csv
from .compute import compute_all_kpis

# Suppress the specific runtime warning
warnings.filterwarnings("ignore", category=RuntimeWarning, 
                       message="'src.csv_report.report.generate' found in sys.modules")

__all__ = ["generate_report"]


def get_template_dir() -> Path:
    """Get the directory containing the template files."""
    return Path(__file__).parent


def generate_report(output_format: str = "markdown") -> str:
    """Generate a report from the computed KPIs.
    
    Args:
        output_format: The format of the output ("markdown" or "html")
        
    Returns:
        The generated report as a string
    """
    # Load and compute data
    df = load_csv()
    kpis = compute_all_kpis(df)
    
    # Set up Jinja2 environment
    template_dir = get_template_dir()
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        autoescape=True
    )
    
    # Load and render template
    template_name = f"template.{output_format}.j2"
    template = env.get_template(template_name)
    
    return template.render(
        base_kpis=kpis["base_kpis"],
        sector_kpis=kpis["sector_kpis"]
    )


def save_report(report: str, output_format: str = "markdown") -> Path:
    """Save the generated report to a file.
    
    Args:
        report: The report content as a string
        output_format: The format of the output ("markdown" or "html")
        
    Returns:
        Path to the saved report file
    """
    # Create reports directory if it doesn't exist
    reports_dir = Path(__file__).parent.parent.parent.parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    # Generate output filename
    output_file = reports_dir / f"sp500_analysis.{output_format}"
    
    # Save the report
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    return output_file


def main() -> None:
    """Generate and save the report."""
    try:
        # Generate markdown report
        report = generate_report("markdown")
        output_file = save_report(report, "markdown")
        print(f"Report generated and saved to: {output_file}")
    except Exception as e:
        print(f"Error generating report: {e}")
        raise


if __name__ == "__main__":
    main()