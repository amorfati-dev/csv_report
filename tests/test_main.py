"""Tests for the main module."""
import pytest
from csv_report.main import parse_args


def test_default_args():
    """Test default argument parsing."""
    args = parse_args([])
    assert args.csv_file == "data/sp500.csv"
    assert args.output == "reports/sp500_report.txt"
    assert args.recipients == []


def test_custom_args():
    """Test custom argument parsing."""
    args = parse_args([
        "--csv-file", "custom.csv",
        "--output", "custom_report.txt",
        "--recipients", "test@example.com"
    ])
    assert args.csv_file == "custom.csv"
    assert args.output == "custom_report.txt"
    assert args.recipients == ["test@example.com"]


def test_invalid_args():
    """Test invalid argument handling."""
    with pytest.raises(SystemExit):
        parse_args(["--invalid-arg"]) 