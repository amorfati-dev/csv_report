#!/usr/bin/env python3
"""Test script for sending HTML emails with inlined CSS."""

import json
import pathlib
from src.csv_report.report.email import send_html_report

def test_send_html_email():
    """Test sending HTML email with inlined CSS."""
    
    # Load test data
    data_file = pathlib.Path("data/dummy.json")
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Test data file not found: {data_file}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return False
    
    # Add report date
    data['report_date'] = "24. Juni 2025"
    
    # Get recipient email from environment or use a test email
    import os
    recipient = os.getenv("REPORT_RECIPIENT")
    
    if not recipient:
        print("⚠️  No REPORT_RECIPIENT environment variable found")
        print("   Please set REPORT_RECIPIENT to your email address")
        print("   Example: export REPORT_RECIPIENT=your.email@example.com")
        return False
    
    try:
        print(f"📧 Sending HTML email to: {recipient}")
        print(f"📊 Report data: {len(data.get('kpis', []))} KPIs")
        
        # Send HTML email
        send_html_report(
            report_data=data,
            recipients=[recipient],
            subject="🧪 Test: HTML Email mit Inline CSS"
        )
        
        print("✅ HTML email sent successfully!")
        print("📱 Check your email client (Gmail/Outlook) to verify rendering")
        return True
        
    except Exception as e:
        print(f"❌ Error sending HTML email: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing HTML email sending with premailer...")
    success = test_send_html_email()
    
    if success:
        print("\n✅ Test completed successfully!")
        print("📸 Don't forget to take screenshots of Gmail and Outlook!")
    else:
        print("\n❌ Test failed!") 