"""Send reports via email using yagmail."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import yagmail
from dotenv import load_dotenv

__all__ = ["send_report"]


def load_env_vars() -> None:
    """Load environment variables from .env file."""
    # Get the project root directory (3 levels up from this file)
    project_root = Path(__file__).parent.parent.parent.parent
    env_path = project_root / '.env'
    
    print(f"Looking for .env file at: {env_path}")
    print(f"File exists: {env_path.exists()}")
    
    if not env_path.exists():
        raise FileNotFoundError(
            f".env file not found at {env_path}. "
            "Please create a .env file with EMAIL_USER, EMAIL_PASSWORD, and REPORT_RECIPIENT."
        )
    
    # Print the contents of the .env file (for debugging)
    print("\nContents of .env file:")
    with open(env_path, 'r') as f:
        print(f.read())
    
    load_dotenv(env_path)
    
    # Debug: Print environment variables (without showing the actual password)
    print("\nEnvironment variables after loading:")
    print(f"EMAIL_USER found: {'Yes' if os.getenv('EMAIL_USER') else 'No'}")
    print(f"EMAIL_PASSWORD found: {'Yes' if os.getenv('EMAIL_PASSWORD') else 'No'}")
    print(f"REPORT_RECIPIENT found: {'Yes' if os.getenv('REPORT_RECIPIENT') else 'No'}")


def send_report(
    report_path: Path,
    recipient: str,
    subject: str = "S&P 500 Companies Analysis Report",
    sender_email: Optional[str] = None,
    sender_password: Optional[str] = None
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
    load_env_vars()
    
    # Get sender credentials from environment variables if not provided
    sender_email = sender_email or os.getenv("EMAIL_USER")
    sender_password = sender_password or os.getenv("EMAIL_PASSWORD")
    
    if not sender_email or not sender_password:
        raise ValueError(
            "Email credentials not provided. Either pass them as arguments "
            "or set EMAIL_USER and EMAIL_PASSWORD in .env file."
        )
    
    print(f"Attempting to send email to: {recipient}")
    
    # Initialize yagmail SMTP connection
    yag = yagmail.SMTP(sender_email, sender_password)
    
    # Send the email
    yag.send(
        to=recipient,
        subject=subject,
        contents=[
            "Please find attached the S&P 500 Companies Analysis Report.",
            str(report_path)
        ]
    )


def main() -> None:
    """Send the latest report via email."""
    try:
        # Load environment variables
        load_env_vars()
        
        # Get the latest report
        reports_dir = Path(__file__).parent.parent.parent.parent / "reports"
        report_path = reports_dir / "sp500_analysis.markdown"
        
        print(f"Looking for report at: {report_path}")
        print(f"Report exists: {report_path.exists()}")
        
        if not report_path.exists():
            raise FileNotFoundError(f"Report not found at {report_path}")
        
        # Get recipient email from environment variable
        recipient = os.getenv("REPORT_RECIPIENT")
        if not recipient:
            raise ValueError("REPORT_RECIPIENT not set in .env file")
        
        # Send the report
        send_report(report_path, recipient)
        print(f"Report sent successfully to {recipient}")
        
    except Exception as e:
        print(f"Error sending report: {e}")
        raise


if __name__ == "__main__":
    main()
