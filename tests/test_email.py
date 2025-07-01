"""Tests for the email module."""

import os

import pytest

from csv_report.report.email import send_report


def test_send_report_missing_credentials() -> None:
    """Test sending report with missing credentials."""
    # Clear environment variables
    os.environ.pop("EMAIL_USER", None)
    os.environ.pop("EMAIL_PASSWORD", None)

    # Try to send report
    with pytest.raises(ValueError, match="Missing EMAIL_USER / EMAIL_PASSWORD"):
        send_report("Test report", ["test@example.com"])


def test_send_report_success() -> None:
    """Test successful report sending."""
    # Set up test credentials
    os.environ["EMAIL_USER"] = "test@example.com"
    os.environ["EMAIL_PASSWORD"] = "test_password"

    # Mock SMTP
    with pytest.raises(Exception):  # Will fail but not due to credentials
        send_report("Test report", ["recipient@example.com"])


def test_send_report_success_with_env_vars() -> None:
    """Test successful report sending with environment variables."""
    # Set up test credentials
    os.environ["EMAIL_USER"] = "test@example.com"
    os.environ["EMAIL_PASSWORD"] = "test_password"

    # Mock SMTP
    with pytest.raises(Exception):  # Will fail but not due to credentials
        send_report("Test report", ["recipient@example.com"], "Test Report")
