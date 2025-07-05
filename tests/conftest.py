import pytest
import subprocess
import os


@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    subprocess.run(
        ["python", "-m", "csv_report.db_init"],
        check=True,
        env=env,
    )
