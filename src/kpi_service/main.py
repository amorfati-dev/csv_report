# src/kpi_service/main.py
import uvicorn

if __name__ == "__main__":
    # ACHTUNG: absoluter Modulpfad, sonst findet Uvicorn dein App-Objekt nicht
    uvicorn.run(
        "kpi_service.app:app",  # ← genau so
        host="127.0.0.1",
        port=8000,
        reload=True,  # Auto-Reload im Dev-Modus
    )
