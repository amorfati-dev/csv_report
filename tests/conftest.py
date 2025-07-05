import pytest
import subprocess

@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    subprocess.run([
        "python", "-m", "csv_report.db_init"
    ], check=True) 