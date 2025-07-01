# src/kpi_service/tests/test_api.py
import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent.parent.parent))

from kpi_service.app import app

client = TestClient(app)


def test_upload_ok() -> None:
    csv = b"Symbol,Shortname,Sector,Marketcap\nAAPL,Apple Inc,Technology,3000000000000\nMSFT,Microsoft Corp,Technology,2500000000000\nGOOGL,Alphabet Inc,Communication Services,2000000000000"
    r = client.post("/upload", files={"file": ("demo.csv", csv, "text/csv")})
    assert r.status_code == 200
    assert r.json()["basic_kpis"]["rows"] == 3


def test_wrong_extension() -> None:
    r = client.post("/upload", files={"file": ("bad.txt", b"dummy", "text/plain")})
    assert r.status_code == 400
