from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from io import StringIO
from .kpi import compute_kpis

app = FastAPI(title="CSV-KPI-Service")


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
