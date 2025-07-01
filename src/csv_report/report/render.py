"""Render HTML reports from data using Jinja2 templates.

This module provides functions to render HTML reports from data
using Jinja2 templates with CSS inlining for email compatibility.
"""

from __future__ import annotations

import json
import pathlib

from jinja2 import Environment, FileSystemLoader, select_autoescape
from premailer import Premailer

BASE_DIR = pathlib.Path(__file__).parent
env = Environment(loader=FileSystemLoader(BASE_DIR), autoescape=select_autoescape())


def render_html_from_data(data: dict) -> str:
    """Render HTML template with data and inline CSS for email compatibility.

    Args:
        data: Dictionary containing data for template rendering

    Returns:
        HTML string with inlined CSS

    """
    # Render template using email-specific template
    tmpl = env.get_template("email_template.html")
    html = tmpl.render(**data)

    # Process with premailer to inline CSS
    p = Premailer(html=html, base_url=None)
    return p.transform()


def render(report_date: str) -> None:
    """Render the HTML report with data from dummy.json."""
    # Load data from dummy.json (located in project root data/ directory)
    data_file = pathlib.Path(
        "/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/"
        "03_side_hussel/04_dev/projekte/csv_report/data/dummy.json",
    )

    try:
        with open(data_file, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return
    except json.JSONDecodeError:
        with open(data_file, encoding="utf-8") as f:
            pass
        return

    # Update the report_date in the data
    data["report_date"] = report_date

    # Render template
    tmpl = env.get_template("report_template.html")
    html = tmpl.render(**data)

    # Save output to reports directory
    output_dir = BASE_DIR.parent.parent.parent / "reports"
    output_dir.mkdir(exist_ok=True)
    out = output_dir / "report_output.html"
    out.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    render("23. Juni 2025")
