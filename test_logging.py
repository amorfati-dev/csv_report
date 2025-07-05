#!/usr/bin/env python3
"""
Test script to demonstrate the logging functionality.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from csv_report.logging_config import setup_cli_logging, get_logger, LoggedOperation
import time


def test_logging():
    """Test the logging functionality."""

    # Setup logging
    logger = setup_cli_logging(log_level="DEBUG")

    logger.info("Starting logging test")

    # Test different log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    # Test context manager for timing
    with LoggedOperation(logger, "Test operation"):
        logger.info("Inside the test operation")
        time.sleep(0.1)  # Simulate some work

    # Test with extra context
    logger.info(
        "User action",
        extra={
            "user_id": 123,
            "action": "test_logging",
            "timestamp": "2025-01-15T10:30:00",
        },
    )

    logger.info("Logging test completed")


if __name__ == "__main__":
    test_logging()
