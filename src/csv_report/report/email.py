"""Email functionality for sending reports.

This module provides functions to send generated reports via email.
"""

from __future__ import annotations

import os
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

__all__ = ["send_report", "send_html_report"]


def send_report(
    report: str, recipients: List[str], subject: Optional[str] = None
) -> None:
    """Send a report via email.

    Args:
        report: The report content to send
        recipients: List of email addresses to send to
        subject: Optional subject line (defaults to "S&P 500 Analysis Report")

    Raises:
        ValueError: If email credentials are missing
        smtplib.SMTPException: If email sending fails
    """
    # Get email credentials from environment
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")

    if not email_user or not email_password:
        raise ValueError("Missing EMAIL_USER / EMAIL_PASSWORD")

    # Create message
    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject or "S&P 500 Analysis Report"

    # Attach report
    msg.attach(MIMEText(report, "plain"))

    # Send email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_user, email_password)
            server.send_message(msg)
    except smtplib.SMTPException as e:
        raise smtplib.SMTPException(f"Failed to send email: {e}")


def send_html_report(
    report_data: dict, recipients: List[str], subject: Optional[str] = None
) -> None:
    """Send an HTML report via email with inlined CSS.

    Args:
        report_data: Dictionary containing report data for template rendering
        recipients: List of email addresses to send to
        subject: Optional subject line (defaults to "S&P 500 Analysis Report")

    Raises:
        ValueError: If email credentials are missing
        smtplib.SMTPException: If email sending fails
    """
    # Get email credentials from environment
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")

    if not email_user or not email_password:
        raise ValueError("Missing EMAIL_USER / EMAIL_PASSWORD")

    # Import render function to generate HTML
    from .render import render_html_from_data

    # Generate HTML with inlined CSS
    html_content = render_html_from_data(report_data)

    # Create message
    msg = MIMEMultipart("alternative")
    msg["From"] = email_user
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject or "S&P 500 Analysis Report"

    # Attach HTML content
    msg.attach(MIMEText(html_content, "html"))

    # Send email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_user, email_password)
            server.send_message(msg)
    except smtplib.SMTPException as e:
        raise smtplib.SMTPException(f"Failed to send HTML email: {e}")


def main() -> None:
    """Send the latest report via email."""
    try:
        # Get the latest report
        reports_dir = Path(__file__).parents[3] / "reports"
        report_file = reports_dir / "sp500_analysis.markdown"

        # Get recipient email from environment variable
        recipient = os.getenv("REPORT_RECIPIENT")
        if not (report_file.exists() and recipient):
            raise SystemExit("Report or REPORT_RECIPIENT missing.")

        # Read the report content
        report_content = report_file.read_text()

        # Send the report
        send_report(report_content, [recipient])
        print(f"✓ Mail sent to {recipient}")

    except Exception as e:
        print(f"Error sending report: {e}")
        raise


if __name__ == "__main__":
    main()
