"""Email functionality for sending reports.

This module provides functions to send generated reports via email.
"""

from __future__ import annotations

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

__all__ = ["send_html_report", "send_report"]


def send_report(
    report: str, recipients: list[str], subject: str | None = None,
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
        msg = "Missing EMAIL_USER / EMAIL_PASSWORD"
        raise ValueError(msg)

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
        msg = f"Failed to send email: {e}"
        raise smtplib.SMTPException(msg)


def send_html_report(
    report_data: dict, recipients: list[str], subject: str | None = None,
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
        msg = "Missing EMAIL_USER / EMAIL_PASSWORD"
        raise ValueError(msg)

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
        msg = f"Failed to send HTML email: {e}"
        raise smtplib.SMTPException(msg)


def main() -> None:
    """Send the latest report via email."""
    try:
        # Get the latest report
        reports_dir = Path(__file__).parents[3] / "reports"
        report_file = reports_dir / "sp500_analysis.markdown"

        # Get recipient email from environment variable
        recipient = os.getenv("REPORT_RECIPIENT")
        if not (report_file.exists() and recipient):
            msg = "Report or REPORT_RECIPIENT missing."
            raise SystemExit(msg)

        # Read the report content
        report_content = report_file.read_text()

        # Send the report
        send_report(report_content, [recipient])

    except Exception:
        raise


if __name__ == "__main__":
    main()
