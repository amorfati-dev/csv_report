"""Send reports via email using yagmail."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import yagmail
from dotenv import load_dotenv, find_dotenv

__all__ = ["send_report"]


def send_report(
    report_path: Path,
    recipient: str,
    subject: str = "S&P 500 Report",
    sender_email: Optional[str] = None,
    sender_password: Optional[str] = None,
) -> None:
    """Send the generated report via email.
    
    Args:
        report_path: Path to the report file
        recipient: Email address of the recipient
        subject: Email subject line
        sender_email: Sender's email address (if None, uses environment variable)
        sender_password: Sender's password (if None, uses environment variable)
    """
    # Load environment variables
    env_path = find_dotenv()
    print(f"Looking for .env file at: {env_path}")
    print(f".env file exists: {Path(env_path).exists() if env_path else False}")
    
    load_dotenv(env_path)
    
    # Debug: Print environment variables (without showing the actual password)
    print("\nEnvironment variables after loading:")
    print(f"EMAIL_USER found: {'Yes' if os.getenv('EMAIL_USER') else 'No'}")
    print(f"EMAIL_PASSWORD found: {'Yes' if os.getenv('EMAIL_PASSWORD') else 'No'}")
    print(f"REPORT_RECIPIENT found: {'Yes' if os.getenv('REPORT_RECIPIENT') else 'No'}")
    
    # Get sender credentials from environment variables if not provided
    sender_email = sender_email or os.getenv("EMAIL_USER")
    sender_password = sender_password or os.getenv("EMAIL_PASSWORD")
    
    if not (sender_email and sender_password):
        raise ValueError("Missing EMAIL_USER / EMAIL_PASSWORD")
    
    if not report_path.exists():
        raise FileNotFoundError(f"Report not found at {report_path}")
    
    print(f"\nAttempting to send email to: {recipient}")
    print(f"Using sender email: {sender_email}")
    
    # Initialize yagmail SMTP connection
    yag = yagmail.SMTP(sender_email, sender_password)
    
    # Send the email
    body = "Attached: latest S&P 500 analysis."
    yag.send(
        to=recipient,
        subject=subject,
        contents=[body, str(report_path)]
    )


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
        send_report(report, recipient)
        print(f"✓ Mail sent to {recipient}")
        
    except Exception as e:
        print(f"Error sending report: {e}")
        raise


if __name__ == "__main__":
    main()
