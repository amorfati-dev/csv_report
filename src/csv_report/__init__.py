"""CSV Report Generator package."""

from .load import load_csv
from .main import app, generate, show_runs, init_db
from .models import Run, Kpi
from .db_init import create_database, get_database_url, test_database_connection
from .database import DatabaseService
from .report.compute import calculate_base_kpis, calculate_sector_kpis
from .report.generate import generate_report, save_report
from .report.email import send_report

__all__ = [
    "load_csv",
    "app",
    "generate",
    "show_runs", 
    "init_db",
    "Run",
    "Kpi",
    "create_database",
    "get_database_url",
    "test_database_connection",
    "DatabaseService",
    "calculate_base_kpis",
    "calculate_sector_kpis",
    "generate_report",
    "save_report",
    "send_report",
]
