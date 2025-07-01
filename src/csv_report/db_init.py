"""Database initialization script for CSV report application."""

from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

from .models import Kpi, Run


def get_database_url() -> str:
    """Get the database URL, defaulting to SQLite."""
    db_path = Path("run.db")
    return f"sqlite:///{db_path}"


def create_database():
    """Create the database and all tables."""
    database_url = get_database_url()
    engine = create_engine(database_url, echo=True)

    # Create all tables
    SQLModel.metadata.create_all(engine)

    return engine


def test_database_connection() -> None:
    """Test the database connection and create a sample record."""
    engine = create_engine(get_database_url())

    with Session(engine) as session:
        # Create a test run
        test_run = Run(
            csv_file="test_data.csv",
            output_format="html",
            status="test",
            rows_processed=10,
        )
        session.add(test_run)
        session.commit()
        session.refresh(test_run)

        # Create a test KPI
        test_kpi = Kpi(
            run_id=test_run.id,
            name="test_kpi",
            value=42.0,
            unit="test_units",
            description="Test KPI for database verification",
        )
        session.add(test_kpi)
        session.commit()

        # Clean up test data
        session.delete(test_kpi)
        session.delete(test_run)
        session.commit()


def main() -> None:
    """Main function to initialize the database."""
    try:
        # Create database and tables
        create_database()

        # Test the connection
        test_database_connection()

    except Exception:
        raise


if __name__ == "__main__":
    main()
