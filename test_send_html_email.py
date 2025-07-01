#!/usr/bin/env python3
"""Test script for sending HTML emails with inlined CSS."""

import json
import pathlib
from typing import Optional

from src.csv_report.report.email import send_html_report


def test_send_html_email() -> Optional[bool]:
    """Test sending HTML email with inlined CSS."""
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

    # Get recipient email from environment or use a test email
    import os

    recipient = os.getenv("REPORT_RECIPIENT")

    if not recipient:
        return False

    try:

        # Send HTML email
        send_html_report(
            report_data=data,
            recipients=[recipient],
            subject="🧪 Test: HTML Email mit Inline CSS",
        )

        return True

    except Exception:
        return False


if __name__ == "__main__":
    success = test_send_html_email()

    if success:
        pass
    else:
        pass
