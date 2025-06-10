import pytest
from pathlib import Path
from src.main import parse_args, send_email

def test_parse_args_default():
    """Test default argument parsing"""
    args = parse_args([])
    assert args.csv is None
    assert args.email is None
    assert args.subject == "CSV Report"

def test_parse_args_custom():
    """Test custom argument parsing"""
    args = parse_args(["--csv", "test.csv", "--email", "test@example.com", "--subject", "Test Subject"])
    assert args.csv == "test.csv"
    assert args.email == "test@example.com"
    assert args.subject == "Test Subject"

def test_send_email(capsys):
    """Test email sending function"""
    send_email("test@example.com", "Test Subject", "Test Body")
    captured = capsys.readouterr()
    assert "To     : test@example.com" in captured.out
    assert "Subject: Test Subject" in captured.out
    assert "Test Body" in captured.out 