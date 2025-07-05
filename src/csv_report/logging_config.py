"""Logging configuration for csv_report tool.

This module provides structured logging configuration for both CLI and FastAPI components.
"""

import logging
import logging.handlers
import sys
import time
from pathlib import Path
from typing import Optional


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_to_console: bool = True,
    component: str = "csv_report",
) -> logging.Logger:
    """Setup logging configuration for the csv_report tool.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
        log_to_console: Whether to log to console
        component: Component name for the logger

    Returns:
        Configured logger instance

    """
    # Create logs directory if it doesn't exist
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

    # Create logger
    logger = logging.getLogger(component)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler with rotation
    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8",  # 10MB
        )
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "csv_report") -> logging.Logger:
    """Get a logger instance with the specified name.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance

    """
    return logging.getLogger(name)


def setup_cli_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup logging specifically for CLI operations.

    Args:
        log_level: Logging level

    Returns:
        Configured CLI logger

    """
    # Determine log file path
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "csv_report_cli.log"

    return setup_logging(
        log_level=log_level,
        log_file=str(log_file),
        log_to_console=True,
        component="csv_report.cli",
    )


def setup_api_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup logging specifically for FastAPI operations.

    Args:
        log_level: Logging level

    Returns:
        Configured API logger

    """
    # Determine log file path
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "csv_report_api.log"

    return setup_logging(
        log_level=log_level,
        log_file=str(log_file),
        log_to_console=False,  # API logs typically go to file only
        component="csv_report.api",
    )


def log_function_call(logger: logging.Logger, func_name: str, **kwargs):
    """Log function call with parameters.

    Args:
        logger: Logger instance
        func_name: Name of the function being called
        **kwargs: Function parameters to log

    """
    logger.debug(f"Calling {func_name} with parameters: {kwargs}")


def log_function_result(
    logger: logging.Logger, func_name: str, result=None, duration: Optional[float] = None,
):
    """Log function result and duration.

    Args:
        logger: Logger instance
        func_name: Name of the function
        result: Function result (optional)
        duration: Execution time in seconds (optional)

    """
    message = f"Function {func_name} completed"
    if duration is not None:
        message += f" in {duration:.2f}s"
    if result is not None:
        message += f" with result: {result}"
    logger.debug(message)


# Context manager for timing operations
class LoggedOperation:
    """Context manager for logging operation timing."""

    def __init__(self, logger: logging.Logger, operation_name: str) -> None:
        self.logger = logger
        self.operation_name = operation_name
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        self.logger.info(f"Starting operation: {self.operation_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        if exc_type is None:
            self.logger.info(
                f"Operation {self.operation_name} completed in {duration:.2f}s",
            )
        else:
            self.logger.error(
                f"Operation {self.operation_name} failed after {duration:.2f}s: {exc_val}",
            )
