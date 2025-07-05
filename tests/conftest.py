import os
import shutil
import subprocess

import pytest


@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    python_path = shutil.which("python")
    if not python_path:
        raise RuntimeError
    subprocess.run(  # noqa: S603
        [python_path, "-m", "csv_report.db_init"],
        check=True,
        env=env,
        shell=False,
    )
