import sys
from io import StringIO
from pathlib import Path
from typing import Annotated, Optional

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile

# Add the csv_report module to the path
sys.path.append(str(Path(__file__).parent.parent))
from csv_report.database import DatabaseService

from .kpi import compute_all_kpis, compute_kpis

app = FastAPI(title="CSV-KPI-Service")


@app.get("/healthz")
async def health_check():
    """Health check endpoint for container monitoring."""
    return {"status": "healthy", "service": "csv-kpi-service"}


@app.post("/upload")
async def upload_csv(file: Annotated[UploadFile, File()] = ...):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Nur CSV akzeptiert")
    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode()))

        # Use enhanced KPI calculation
        all_kpis = compute_all_kpis(df)

        return {
            "filename": file.filename,
            "basic_kpis": compute_kpis(df),  # Legacy basic KPIs
            "enhanced_kpis": all_kpis,  # New comprehensive KPIs
        }
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Parsing-Fehler: {exc}")


@app.get("/runs")
async def get_runs(limit: Optional[int] = 10, run_id: Optional[int] = None):
    """Get CSV report generation runs from the database."""
    db_service = DatabaseService()

    if run_id:
        # Return specific run details
        run = db_service.get_run_by_id(run_id)
        if not run:
            raise HTTPException(
                status_code=404, detail=f"Run with ID {run_id} not found",
            )

        # Get KPIs for this run
        kpis = db_service.get_kpis_for_run(run.id)

        return {
            "run": {
                "id": run.id,
                "timestamp": run.timestamp.isoformat(),
                "csv_file": run.csv_file,
                "output_format": run.output_format,
                "status": run.status,
                "rows_processed": run.rows_processed,
                "error_message": run.error_message,
            },
            "kpis": [
                {
                    "name": kpi.name,
                    "value": kpi.value,
                    "unit": kpi.unit,
                    "description": kpi.description,
                    "calculated_at": kpi.calculated_at.isoformat(),
                }
                for kpi in kpis
            ],
        }
    # Return recent runs summary
    runs = db_service.get_recent_runs(limit)

    return {
        "runs": [
            {
                "id": run.id,
                "timestamp": run.timestamp.isoformat(),
                "csv_file": run.csv_file,
                "output_format": run.output_format,
                "status": run.status,
                "rows_processed": run.rows_processed,
                "error_message": run.error_message,
            }
            for run in runs
        ],
        "total_count": len(runs),
    }
