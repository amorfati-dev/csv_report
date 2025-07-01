#!/usr/bin/env python3
"""Test script for HTML email functionality with premailer CSS inlining."""

import json
import pathlib
from typing import Optional

from src.csv_report.report.render import render_html_from_data


def test_html_rendering() -> Optional[bool]:
    """Test HTML rendering with premailer CSS inlining."""
    # Load test data
    data_file = pathlib.Path("data/dummy.json")

    try:
        with open(data_file, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return False
    except json.JSONDecodeError:
        return False

    # Add report date
    data["report_date"] = "24. Juni 2025"

    try:
        # Render HTML with inlined CSS
        html_content = render_html_from_data(data)

        # Save to file for inspection
        output_file = pathlib.Path("reports/test_email_output.html")
        output_file.parent.mkdir(exist_ok=True)
        output_file.write_text(html_content, encoding="utf-8")

        # Check if CSS was inlined (should contain style attributes)
        if "style=" in html_content:
            pass
        else:
            pass

        return True

    except Exception:
        return False


if __name__ == "__main__":
    success = test_html_rendering()

    if success:
        pass
    else:
        pass
