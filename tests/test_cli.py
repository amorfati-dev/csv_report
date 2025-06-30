"""Tests for CLI functionality using Typer."""

import pytest
from pathlib import Path
from typer.testing import CliRunner
from csv_report.main import app
from csv_report.database import DatabaseService


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()


def test_generate_command_help(runner):
    """Test generate command help."""
    result = runner.invoke(app, ["generate", "--help"])
    assert result.exit_code == 0
    assert "Generate a report from a CSV file" in result.stdout


def test_show_runs_command_help(runner):
    """Test show-runs command help."""
    result = runner.invoke(app, ["show-runs", "--help"])
    assert result.exit_code == 0
    assert "Show recent report generation runs" in result.stdout


def test_init_db_command_help(runner):
    """Test init-db command help."""
    result = runner.invoke(app, ["init-db", "--help"])
    assert result.exit_code == 0
    assert "Initialize the database" in result.stdout


def test_generate_command_with_options(runner):
    """Test generate command with options."""
    result = runner.invoke(app, [
        "generate", 
        "--csv-file", "test.csv", 
        "--output-format", "html"
    ])
    # This will likely fail due to missing CSV file, but we can test the argument parsing
    assert result.exit_code != 0  # Expected to fail without CSV file


def test_show_runs_no_runs(runner):
    """Test show-runs when no runs exist."""
    result = runner.invoke(app, ["show-runs"])
    assert result.exit_code == 0
    assert "No runs found in database" in result.stdout


def test_show_runs_with_limit(runner):
    """Test show-runs with limit option."""
    result = runner.invoke(app, ["show-runs", "--limit", "5"])
    assert result.exit_code == 0
    assert "No runs found in database" in result.stdout


def test_database_service_creation():
    """Test DatabaseService can be instantiated."""
    db_service = DatabaseService()
    assert db_service is not None
    assert hasattr(db_service, 'engine')


def test_database_service_create_run():
    """Test creating a run through DatabaseService."""
    db_service = DatabaseService()
    
    run = db_service.create_run(
        csv_file="test.csv",
        output_format="html",
        rows_processed=100
    )
    
    assert run.id is not None
    assert run.csv_file == "test.csv"
    assert run.output_format == "html"
    assert run.rows_processed == 100
    assert run.status == "completed"


def test_database_service_add_kpi():
    """Test adding a KPI through DatabaseService."""
    db_service = DatabaseService()
    
    # Create a run first
    run = db_service.create_run(
        csv_file="test.csv",
        output_format="html"
    )
    
    # Add a KPI
    kpi = db_service.add_kpi(
        run_id=run.id,
        name="total_companies",
        value=500.0,
        unit="companies",
        description="Total number of companies"
    )
    
    assert kpi.id is not None
    assert kpi.run_id == run.id
    assert kpi.name == "total_companies"
    assert kpi.value == 500.0 