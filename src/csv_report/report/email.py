"""Email functionality for sending reports.

This module provides functions to send generated reports via email.
"""
from __future__ import annotations

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List

__all__ = ["send_report"]


def send_report(
    report: str,
    recipients: List[str],
    subject: Optional[str] = None
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


def main() -> None:
    """Send the latest report via email."""
    try:
        # Get the latest report
        reports_dir = Path(__file__).parents[3] / "reports"
        report = reports_dir / "sp500_analysis.markdown"
        
        # Get recipient email from environment variable
        recipient = os.getenv("REPORT_RECIPIENT")
        if not (report.exists() and recipient):
            raise SystemExit("Report or REPORT_RECIPIENT missing.")
        
        # Send the report
        send_report(str(report), [recipient])
        print(f"✓ Mail sent to {recipient}")
        
    except Exception as e:
        print(f"Error sending report: {e}")
        raise


if __name__ == "__main__":
    main()
