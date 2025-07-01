import contextlib
import os

from dotenv import load_dotenv

from csv_report.email_sender import EmailSender

# Load environment variables
load_dotenv()


def test_email() -> None:
    # Get email configuration from environment variables
    sender_email = os.getenv("EMAIL_USER")
    app_password = os.getenv("EMAIL_PASSWORD")
    recipient_email = os.getenv(
        "RECIPIENT_EMAIL", sender_email,
    )  # Default to sender if not specified

    if not all([sender_email, app_password]):
        return

    # Create email sender instance
    email_sender = EmailSender(sender_email=sender_email, app_password=app_password)

    # Send test email
    subject = "Test Email from csv_report"
    body = """
    <html>
        <body>
            <h1>Test Email</h1>
            <p>This is a test email sent from the csv_report package.</p>
            <p>If you're receiving this, the email functionality is working correctly!</p>
        </body>
    </html>
    """

    with contextlib.suppress(Exception):
        email_sender.send_email(
            recipient_email=recipient_email, subject=subject, body=body,
        )


if __name__ == "__main__":
    test_email()
