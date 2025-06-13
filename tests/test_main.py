"""Tests for the main module."""
import pytest
from csv_report.main import parse_args


def test_parse_args_default():
    """Test argument parsing with default values."""
    args = parse_args([])
    assert args.csv_file is None
    assert args.output_format == "markdown"


def test_parse_args_custom():
    """Test argument parsing with custom values."""
    args = parse_args(["--csv-file", "test.csv", "--output-format", "html"])
    assert args.csv_file == "test.csv"
    assert args.output_format == "html"


def test_parse_args_system_exit():
    """Test argument parsing with invalid values."""
    with pytest.raises(SystemExit):
        parse_args(["--output-format", "invalid"]) 