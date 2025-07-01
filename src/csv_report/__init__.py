"""CSV Report Generator package."""

from .database import DatabaseService
from .db_init import create_database, get_database_url, test_database_connection
from .load import load_csv
from .main import app, generate, init_db, show_runs
from .models import Kpi, Run
from .report.email import send_report

# KPI functions now available from kpi_service module
from .report.generate import generate_report, save_report

__all__ = [
    "DatabaseService",
    "Kpi",
    "Run",
    "app",
    "create_database",
    "generate",
    # KPI functions moved to kpi_service module
    "generate_report",
    "get_database_url",
    "init_db",
    "load_csv",
    "save_report",
    "send_report",
    "show_runs",
    "test_database_connection",
]
