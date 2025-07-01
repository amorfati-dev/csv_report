"""Database service for CSV report application."""

from typing import Optional

from sqlmodel import Session, create_engine, select

from .db_init import get_database_url
from .models import Kpi, Run


class DatabaseService:
    """Service class for database operations."""

    def __init__(self) -> None:
        self.engine = create_engine(get_database_url(), echo=False)

    def create_run(
        self,
        csv_file: str,
        output_format: str,
        rows_processed: Optional[int] = None,
        status: str = "completed",
        error_message: Optional[str] = None,
    ) -> Run:
        """Create a new run record in the database."""
        with Session(self.engine) as session:
            run = Run(
                csv_file=csv_file,
                output_format=output_format,
                rows_processed=rows_processed,
                status=status,
                error_message=error_message,
            )
            session.add(run)
            session.commit()
            session.refresh(run)
            return run

    def add_kpi(
        self,
        run_id: int,
        name: str,
        value: float,
        unit: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Kpi:
        """Add a KPI record linked to a run."""
        with Session(self.engine) as session:
            kpi = Kpi(
                run_id=run_id,
                name=name,
                value=value,
                unit=unit,
                description=description,
            )
            session.add(kpi)
            session.commit()
            session.refresh(kpi)
            return kpi

    def get_all_runs(self) -> list[Run]:
        """Get all runs from the database."""
        with Session(self.engine) as session:
            statement = select(Run).order_by(Run.timestamp.desc())
            return session.exec(statement).all()

    def get_run_by_id(self, run_id: int) -> Optional[Run]:
        """Get a specific run by ID."""
        with Session(self.engine) as session:
            statement = select(Run).where(Run.id == run_id)
            return session.exec(statement).first()

    def get_kpis_for_run(self, run_id: int) -> list[Kpi]:
        """Get all KPIs for a specific run."""
        with Session(self.engine) as session:
            statement = select(Kpi).where(Kpi.run_id == run_id)
            return session.exec(statement).all()

    def get_recent_runs(self, limit: int = 10) -> list[Run]:
        """Get the most recent runs."""
        with Session(self.engine) as session:
            statement = select(Run).order_by(Run.timestamp.desc()).limit(limit)
            return session.exec(statement).all()
