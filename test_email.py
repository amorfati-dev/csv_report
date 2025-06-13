from csv_report.email_sender import EmailSender
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_email():
    # Get email configuration from environment variables
    sender_email = os.getenv('EMAIL_USER')
    app_password = os.getenv('EMAIL_PASSWORD')
    recipient_email = os.getenv('RECIPIENT_EMAIL', sender_email)  # Default to sender if not specified
    
    if not all([sender_email, app_password]):
        print("Error: Please set EMAIL_USER and EMAIL_PASSWORD in .env file")
        return
    
    # Create email sender instance
    email_sender = EmailSender(
        sender_email=sender_email,
        app_password=app_password
    )
    
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
    
    try:
        email_sender.send_email(
            recipient_email=recipient_email,
            subject=subject,
            body=body
        )
        print(f"Test email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

if __name__ == "__main__":
    test_email() 