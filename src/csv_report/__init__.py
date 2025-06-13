"""CSV Report Generator package."""

from .load import DataLoadError, load_csv
from .main import main

__version__ = "0.1.0"
__all__ = ["DataLoadError", "load_csv", "main"] 