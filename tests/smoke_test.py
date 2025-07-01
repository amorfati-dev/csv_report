import requests

BASE = "http://localhost:8000"


def test_health() -> None:
    assert requests.get(f"{BASE}/health").status_code == 200


def test_docs() -> None:
    assert requests.get(f"{BASE}/docs").status_code == 200


def test_sample() -> None:
    r = requests.get(f"{BASE}/api/v1/resource?id=42")
    assert r.status_code == 200
    assert "id" in r.json()
