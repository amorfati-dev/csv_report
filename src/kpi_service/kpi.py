import pandas as pd


def compute_kpis(df: pd.DataFrame) -> dict:
    numeric = df.select_dtypes("number")
    return {
        "rows": len(df),
        "cols": len(df.columns),
        "means": numeric.mean().round(2).to_dict(),  # bsp-KPI
    }
