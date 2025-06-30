"""Tests for database models."""

import pytest
from datetime import datetime
from sqlmodel import Session, create_engine
from csv_report.models import Run, Kpi


@pytest.fixture
def engine():
    """Create a test database engine."""
    return create_engine("sqlite:///:memory:", echo=False)


@pytest.fixture
def session(engine):
    """Create a test database session."""
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_run_model_creation(session):
    """Test creating a Run model."""
    run = Run(
        csv_file="test.csv",
        output_format="html",
        status="completed",
        rows_processed=100
    )
    
    session.add(run)
    session.commit()
    session.refresh(run)
    
    assert run.id is not None
    assert run.csv_file == "test.csv"
    assert run.output_format == "html"
    assert run.status == "completed"
    assert run.rows_processed == 100
    assert isinstance(run.timestamp, datetime)


def test_kpi_model_creation(session):
    """Test creating a Kpi model."""
    # First create a run
    run = Run(csv_file="test.csv", output_format="html")
    session.add(run)
    session.commit()
    session.refresh(run)
    
    # Then create a KPI linked to that run
    kpi = Kpi(
        run_id=run.id,
        name="total_companies",
        value=500.0,
        unit="companies",
        description="Total number of companies"
    )
    
    session.add(kpi)
    session.commit()
    session.refresh(kpi)
    
    assert kpi.id is not None
    assert kpi.run_id == run.id
    assert kpi.name == "total_companies"
    assert kpi.value == 500.0
    assert kpi.unit == "companies"
    assert kpi.description == "Total number of companies"
    assert isinstance(kpi.calculated_at, datetime)


def test_run_kpi_relationship(session):
    """Test the relationship between Run and Kpi models."""
    # Create a run
    run = Run(csv_file="test.csv", output_format="html")
    session.add(run)
    session.commit()
    session.refresh(run)
    
    # Create multiple KPIs for the same run
    kpi1 = Kpi(run_id=run.id, name="total_companies", value=500.0)
    kpi2 = Kpi(run_id=run.id, name="avg_market_cap", value=1000000.0)
    
    session.add_all([kpi1, kpi2])
    session.commit()
    
    # Verify both KPIs are linked to the same run
    assert kpi1.run_id == run.id
    assert kpi2.run_id == run.id
    assert kpi1.id != kpi2.id 