"""Database models for CSV report application using SQLModel."""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Run(SQLModel, table=True):
    """Model representing a CSV report generation run."""

    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    csv_file: str = Field(description="Path to the CSV file that was processed")
    output_format: str = Field(description="Output format (markdown, html)")
    status: str = Field(default="completed", description="Status of the run")
    rows_processed: Optional[int] = Field(
        default=None,
        description="Number of rows processed",
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if failed",
    )
    duration: Optional[float] = Field(
        default=None,
        description="Duration of the run in seconds",
    )

    class Config:
        schema_extra = {
            "example": {
                "csv_file": "data/sp500.csv",
                "output_format": "html",
                "status": "completed",
                "rows_processed": 500,
                "error_message": None,
            },
        }


class Kpi(SQLModel, table=True):
    """Model representing KPIs calculated from CSV data."""

    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    run_id: int = Field(
        foreign_key="run.id",
        description="Reference to the run that generated this KPI",
    )
    name: str = Field(description="Name of the KPI")
    value: float = Field(description="Calculated value of the KPI")
    unit: Optional[str] = Field(default=None, description="Unit of measurement")
    description: Optional[str] = Field(
        default=None,
        description="Description of what this KPI measures",
    )
    calculated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "run_id": 1,
                "name": "total_companies",
                "value": 500.0,
                "unit": "companies",
                "description": "Total number of companies in the dataset",
            },
        }
