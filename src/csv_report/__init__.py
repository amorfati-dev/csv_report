"""CSV Report Generator package."""

from .load import load_csv
from .main import parse_args
from .report.compute import calculate_base_kpis, calculate_sector_kpis
from .report.generate import generate_report, save_report
from .report.email import send_report

__all__ = [
    "load_csv",
    "parse_args",
    "calculate_base_kpis",
    "calculate_sector_kpis",
    "generate_report",
    "save_report",
    "send_report"
] 