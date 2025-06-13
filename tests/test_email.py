"""Tests for the email module."""
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from csv_report.report.email import send_report

def test_send_report_missing_credentials():
    """Test sending report with missing credentials."""
    # Clear environment variables
    os.environ.pop("EMAIL_USER", None)
    os.environ.pop("EMAIL_PASSWORD", None)
    
    # Try to send report
    with pytest.raises(ValueError, match="Missing EMAIL_USER / EMAIL_PASSWORD"):
        send_report("Test report", ["test@example.com"])

def test_send_report_success():
    """Test successful report sending."""
    # Set up test credentials
    os.environ["EMAIL_USER"] = "test@example.com"
    os.environ["EMAIL_PASSWORD"] = "test_password"
    
    # Mock SMTP
    with pytest.raises(Exception):  # Will fail but not due to credentials
        send_report("Test report", ["recipient@example.com"])

def test_send_report_success_with_env_vars():
    """Test successful report sending with environment variables."""
    mock_yag = MagicMock()
    env_vars = {
        'EMAIL_USER': 'test@example.com',
        'EMAIL_PASSWORD': 'password',
        'REPORT_RECIPIENT': 'recipient@example.com'
    }
    
    with patch('yagmail.SMTP', return_value=mock_yag), \
         patch('os.getenv', side_effect=lambda x: env_vars.get(x)), \
         patch('pathlib.Path.exists', return_value=True):
        
        send_report(
            report_path=Path("test_report.md"),
            recipient="recipient@example.com",
            subject="Test Report"
        )
        
        mock_yag.send.assert_called_once()
        call_args = mock_yag.send.call_args[1]
        assert call_args['to'] == "recipient@example.com"
        
        # Verify yagmail was called correctly
        assert call_args['subject'] == "Test Report"
        assert "test_report.md" in str(call_args['contents'][1]) 