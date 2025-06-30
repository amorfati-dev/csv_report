"""Database initialization script for CSV report application."""

import os
from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session
from .models import Run, Kpi


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
    
    print(f"✅ Database created successfully at: {get_database_url()}")
    print("📋 Tables created:")
    print("   - run (for tracking CSV report generation runs)")
    print("   - kpi (for storing calculated KPIs)")
    
    return engine


def test_database_connection():
    """Test the database connection and create a sample record."""
    engine = create_engine(get_database_url())
    
    with Session(engine) as session:
        # Create a test run
        test_run = Run(
            csv_file="test_data.csv",
            output_format="html",
            status="test",
            rows_processed=10
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
            description="Test KPI for database verification"
        )
        session.add(test_kpi)
        session.commit()
        
        print("✅ Database connection test successful!")
        print(f"   Created test run with ID: {test_run.id}")
        print(f"   Created test KPI with ID: {test_kpi.id}")
        
        # Clean up test data
        session.delete(test_kpi)
        session.delete(test_run)
        session.commit()
        print("🧹 Test data cleaned up")


def main():
    """Main function to initialize the database."""
    try:
        print("🚀 Initializing CSV Report Database...")
        
        # Create database and tables
        engine = create_database()
        
        # Test the connection
        test_database_connection()
        
        print("\n🎉 Database initialization completed successfully!")
        print(f"📁 Database file: {Path('run.db').absolute()}")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        raise


if __name__ == "__main__":
    main() 