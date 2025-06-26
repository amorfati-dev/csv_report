from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from io import StringIO
from .kpi import compute_kpis

app = FastAPI(title="CSV-KPI-Service")


@app.get("/healthz")
async def health_check():
    """Health check endpoint for container monitoring"""
    return {"status": "healthy", "service": "csv-kpi-service"}


@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Nur CSV akzeptiert")
    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode()))
        kpis = compute_kpis(df)
        return {"filename": file.filename, "kpis": kpis}
    except Exception as exc:
        print(f"Caught exception: {exc}")
        raise HTTPException(status_code=422, detail=f"Parsing-Fehler: {exc}")
