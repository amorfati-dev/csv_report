import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from csv_report.report.email import send_report, load_env_vars

def test_load_env_vars_missing_file():
    """Test loading environment variables when .env file is missing."""
    with pytest.raises(FileNotFoundError):
        with patch('pathlib.Path.exists', return_value=False):
            load_env_vars()

def test_send_report_missing_credentials():
    """Test sending report with missing credentials."""
    with pytest.raises(ValueError, match="Email credentials not provided"):
        with patch('os.getenv', return_value=None):
            send_report(
                report_path=Path("test_report.md"),
                recipient="test@example.com"
            )

def test_send_report_success():
    """Test successful report sending."""
    mock_yag = MagicMock()
    with patch('yagmail.SMTP', return_value=mock_yag), \
         patch('os.getenv', side_effect=['test@example.com', 'password']), \
         patch('pathlib.Path.exists', return_value=True):
        
        send_report(
            report_path=Path("test_report.md"),
            recipient="recipient@example.com",
            subject="Test Report"
        )
        
        # Verify yagmail was called correctly
        mock_yag.send.assert_called_once()
        call_args = mock_yag.send.call_args[1]
        assert call_args['to'] == "recipient@example.com"
        assert call_args['subject'] == "Test Report"
        assert "test_report.md" in str(call_args['contents'][1]) 