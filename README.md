# CSV Report Generator

A comprehensive CLI tool and FastAPI service for analyzing CSV data, generating reports, and tracking performance metrics.

## Features

- **CLI Tool**: Generate reports from CSV files with database tracking
- **FastAPI Service**: REST API for CSV analysis and run history
- **Database Persistence**: Store run metadata and calculated KPIs
- **Multiple Output Formats**: Markdown and HTML reports
- **Email Integration**: Send reports via email (optional)

## Quick Start

### CLI Tool

```bash
# Install
pip install csv-report

# Generate a report
csv-report generate --csv-file data/sp500_companies.csv --output-format html

# View recent runs
csv-report show-runs --limit 5

# View specific run details
csv-report show-runs --run-id 1
```

### FastAPI Service

```bash
# Start the service
uvicorn kpi_service.app:app --reload

# Upload CSV for analysis
curl -F "file=@data/sp500_companies.csv" http://127.0.0.1:8000/upload

# Get run history
curl http://127.0.0.1:8000/runs

# Get specific run details
curl http://127.0.0.1:8000/runs?run_id=1
```

## Data Flow

```mermaid
graph TD
    A[CSV File] --> B[CLI Tool]
    A --> C[FastAPI Service]
    
    B --> D[Load & Parse CSV]
    D --> E[Calculate KPIs]
    E --> F[Generate Report]
    F --> G[Save Report File]
    E --> H[Save to Database]
    H --> I[Run Metadata]
    H --> J[KPI Records]
    
    C --> K[Upload Endpoint]
    K --> L[Quick KPI Analysis]
    L --> M[Return JSON]
    
    N[Database] --> O[/runs Endpoint]
    O --> P[Return Run History]
    
    subgraph "Database Tables"
        I
        J
    end
    
    subgraph "CLI Pipeline"
        D
        E
        F
        G
        H
    end
    
    subgraph "FastAPI Endpoints"
        K
        L
        M
        O
        P
    end
```

## CLI Commands

### `generate`
Generate a report from CSV data and store run metadata in database.

```bash
csv-report generate [OPTIONS]

Options:
  --csv-file, -f TEXT     Path to the CSV file to analyze
  --output-format, -o     Format of the output report [markdown|html]
  --output TEXT           Output file path (default: reports/sp500_analysis.{format})
```

### `show-runs`
Display recent report generation runs from the database.

```bash
csv-report show-runs [OPTIONS]

Options:
  --limit, -l INTEGER     Number of recent runs to show [default: 10]
  --run-id, -r INTEGER    Show details for a specific run ID
```

### `init-db`
Initialize the database and create tables.

```bash
csv-report init-db
```

## FastAPI Endpoints

### `POST /upload`
Upload a CSV file for quick KPI analysis.

**Request:**
```bash
curl -F "file=@data.csv" http://127.0.0.1:8000/upload
```

**Response:**
```json
{
  "filename": "data.csv",
  "kpis": {
    "rows": 503,
    "cols": 16,
    "means": {
      "Currentprice": 227.4,
      "Marketcap": 112231944591.01
    }
  }
}
```

### `GET /runs`
Get CSV report generation runs from the database.

**Query Parameters:**
- `limit` (optional): Number of runs to return (default: 10)
- `run_id` (optional): Get details for specific run ID

**Response (list):**
```json
{
  "runs": [
    {
      "id": 1,
      "timestamp": "2025-01-01T12:00:00",
      "csv_file": "sp500_companies.csv",
      "output_format": "html",
      "status": "completed",
      "rows_processed": 503,
      "error_message": null
    }
  ],
  "total_count": 1
}
```

**Response (specific run):**
```json
{
  "run": {
    "id": 1,
    "timestamp": "2025-01-01T12:00:00",
    "csv_file": "sp500_companies.csv",
    "output_format": "html",
    "status": "completed",
    "rows_processed": 503,
    "error_message": null
  },
  "kpis": [
    {
      "name": "total_companies",
      "value": 503.0,
      "unit": "companies",
      "description": "Total number of companies in the dataset",
      "calculated_at": "2025-01-01T12:00:00"
    }
  ]
}
```

### `GET /healthz`
Health check endpoint for container monitoring.

**Response:**
```json
{
  "status": "healthy",
  "service": "csv-kpi-service"
}
```

## Database Schema

### Run Table
Stores metadata about each CSV report generation run.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| timestamp | DATETIME | When the run was executed |
| csv_file | TEXT | Path to the input CSV file |
| output_format | TEXT | Report format (markdown/html) |
| status | TEXT | Run status (processing/completed/failed) |
| rows_processed | INTEGER | Number of rows processed |
| error_message | TEXT | Error message if failed |

### KPI Table
Stores calculated key performance indicators for each run.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| run_id | INTEGER | Foreign key to run table |
| name | TEXT | KPI name |
| value | FLOAT | Calculated value |
| unit | TEXT | Unit of measurement |
| description | TEXT | Description of the KPI |
| calculated_at | DATETIME | When the KPI was calculated |

## Calculated KPIs

The system automatically calculates and stores the following KPIs:

### Base KPIs
- `total_companies`: Total number of companies
- `avg_market_cap`: Average market capitalization
- `median_market_cap`: Median market capitalization

### Market Cap Distribution
- `small_cap_count`: Companies with <$2B market cap
- `mid_cap_count`: Companies with $2B-$10B market cap
- `large_cap_count`: Companies with $10B-$100B market cap
- `mega_cap_count`: Companies with >$100B market cap

### Sector Analysis
- `tech_companies`: Number of technology sector companies
- `tech_market_cap`: Total market cap of technology companies

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment.

### Automated Checks

Every push and pull request triggers:

- **Code Formatting**: Black ensures consistent code style
- **Linting**: Ruff checks for code quality and potential issues
- **Security Scanning**: Bandit and Safety check for vulnerabilities
- **Testing**: Pytest runs all tests with coverage reporting
- **FastAPI Tests**: Separate test suite for API endpoints
- **Docker Build**: Automated container builds for main branch

### Local Development

Install pre-commit hooks for local quality assurance:

```bash
# Install pre-commit
poetry install --with dev

# Install git hooks
pre-commit install

# Run all checks manually
pre-commit run --all-files
```

### Manual Checks

```bash
# Format code
poetry run black .

# Lint code
poetry run ruff check .

# Check security
poetry run bandit -r src/
poetry run safety check

# Run tests
poetry run pytest --cov=src tests/
```

## Installation

### Development Setup

```bash
# Clone repository
git clone <your-repo-url>
cd csv_report

# Install dependencies
poetry install

# Initialize database
poetry run csv-report init-db

# Run tests
poetry run pytest
```

### Production Deployment

The service is deployed on Fly.io at [https://csv-report.fly.dev](https://csv-report.fly.dev).

```bash
# Deploy updates
fly deploy

# Check health
curl https://csv-report.fly.dev/healthz
```

## Requirements

- Python 3.12+
- pandas
- sqlmodel
- fastapi
- typer
- rich
- jinja2

## License

MIT License