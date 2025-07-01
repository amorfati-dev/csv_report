"""Tests for the main module."""

from typer.testing import CliRunner

from csv_report.main import app


def test_generate_command_help() -> None:
    """Test that the generate command shows help."""
    runner = CliRunner()
    result = runner.invoke(app, ["generate", "--help"])
    assert result.exit_code == 0
    assert "Generate a report from a CSV file" in result.output


def test_show_runs_command_help() -> None:
    """Test that the show-runs command shows help."""
    runner = CliRunner()
    result = runner.invoke(app, ["show-runs", "--help"])
    assert result.exit_code == 0
    assert "Show recent report generation runs" in result.output


def test_init_db_command_help() -> None:
    """Test that the init-db command shows help."""
    runner = CliRunner()
    result = runner.invoke(app, ["init-db", "--help"])
    assert result.exit_code == 0
    assert "Initialize the database" in result.output
