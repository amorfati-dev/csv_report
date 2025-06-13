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


def generate_report(data: pd.DataFrame) -> str:
    """Generate a report from the DataFrame.

    Args:
        data: DataFrame containing the analysis data

    Returns:
        Generated report as a string
    """
    # Initialize Jinja2 environment
    template_dir = Path(__file__).parent
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        autoescape=True
    )
    
    # Load and render template
    template = env.get_template("template.j2")
    return template.render(data=data)


def save_report(report: str, output_path: Path) -> Path:
    """Save the generated report to a file.

    Args:
        report: The report content as a string
        output_path: The path where to save the report

    Returns:
        Path to the saved report file
    """
    # Create parent directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the report
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    return output_path


def main() -> None:
    """Generate and save the report."""
    try:
        # Generate markdown report
        df = load_csv()
        report = generate_report(df)
        output_file = save_report(report, Path("reports/sp500_analysis.markdown"))
        print(f"Report generated and saved to: {output_file}")
    except Exception as e:
        print(f"Error generating report: {e}")
        raise


if __name__ == "__main__":
    main()