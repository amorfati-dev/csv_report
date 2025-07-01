"""Tests for the main module."""

import pytest

from csv_report.main import parse_args


def test_default_args() -> None:
    """Test default argument parsing."""
    args = parse_args([])
    assert args.csv_file is None
    assert args.output_format == "markdown"


def test_custom_args() -> None:
    """Test custom argument parsing."""
    args = parse_args(["--csv-file", "custom.csv", "--output-format", "markdown"])
    assert args.csv_file == "custom.csv"
    assert args.output_format == "markdown"


def test_invalid_args() -> None:
    """Test invalid argument handling."""
    with pytest.raises(SystemExit):
        parse_args(["--invalid-arg"])
