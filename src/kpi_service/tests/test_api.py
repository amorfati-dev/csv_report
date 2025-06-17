# src/kpi_service/tests/test_api.py
from fastapi.testclient import TestClient
from kpi_service.app import app  # Pfad ggf. anpassen

client = TestClient(app)


def test_upload_ok():
    csv = b"a,b\n1,2\n"
    r = client.post("/upload", files={"file": ("demo.csv", csv, "text/csv")})
    assert r.status_code == 200
    assert r.json()["kpis"]["rows"] == 1


def test_wrong_extension():
    r = client.post("/upload", files={"file": ("bad.txt", b"dummy", "text/plain")})
    assert r.status_code == 400
