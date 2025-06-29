# csv_report

Kleines CLI-Tool, das CSV-Daten auswertet und einen Report mailt.

## Quick-Start

### 1. Installation (als End-User)

> Voraussetzung: **Python ≥ 3.12** ist installiert.

```bash
# Empfohlen – sauber isoliert per pipx
python3 -m pip install --user pipx
pipx ensurepath
pipx install csv-report

<details> <summary>Alternative: Poetry-basierte Entwicklungsversion (Editable Install)</summary>
git clone https://github.com/amorfati-dev/csv_report
cd csv_report
poetry install             # installiert Dependencies + das Paket selbst
poetry run csv-report --help
</details>


2. pipErster Report
csv-report \
  --csv-file examples/sales_q1.csv \
  --output-format html \
  > report.html

  | Option            | Bedeutung                        |
| ----------------- | -------------------------------- |
| `--csv-file`      | Pfad zur Eingabe-CSV             |
| `--output-format` | `markdown` (Default) oder `html` |


Mail-Versand aktivieren:
Lege eine .env an (oder setze Umgebungs­variablen)<br>
EMAIL_USER, EMAIL_PASSWORD, EMAIL_TO – danach wird die generierte Datei per Gmail versendet.

3. Hilfe anzeigen

csv-report --help


---

## 2 — Commit & Push

```bash
git add README.md
git commit -m "docs: add Quick-Start section with install & usage"
git push origin main



## Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd csv_report
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies in editable mode:
   ```bash
   pip install -e . --break-system-packages
   ```

## Usage

Run the CLI tool with:
```bash
csv_report --csv data/sp500_companies.csv
```

## Requirements
- Python 3.9+
- pandas

## Example Output
```
Report for S&P 500 Companies
-------------------------------------------
Total Companies: 503
Top Companies:
  Symbol              Shortname      Marketcap
0   AAPL             Apple Inc.  3745241628672
1   NVDA     NVIDIA Corporation  3307864588288
2   MSFT  Microsoft Corporation  3296105332736
3   AMZN       Amazon.com, Inc.  2366295506944
4  GOOGL          Alphabet Inc.  2276776214528
Sector Distribution:
Sector
Technology            82
Industrials           70
Financial Services    67
Healthcare            63
Consumer Cyclical     55
Name: count, dtype: int64
```

# CSV-KPI-Service

Minimaler FastAPI-Microservice, der eine hochgeladene CSV analysiert und Key-Performance-Indikatoren (KPIs) als JSON zurückgibt.

## Quick Start

```bash
# 1) Environment starten
poetry install
poetry run uvicorn kpi_service.app:app --reload

# 2) Datei hochladen
curl -F "file=@sample.csv" http://127.0.0.1:8000/upload

{
  "rows": 503,
  "cols": 16,
  "means": {
    "Currentprice": 227.4,
    "Marketcap": 112231944591.01
  }
}

poetry run pytest -q


poetry run black .
poetry run ruff check .


FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-dev
COPY src ./src
CMD ["uvicorn", "kpi_service.app:app", "--host", "0.0.0.0", "--port", "8000"]


