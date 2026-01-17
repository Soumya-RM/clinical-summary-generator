import pandas as pd
from typing import List, Dict, Any

def normalize_vitals(vitals: List[Dict[str, Any]]) -> pd.DataFrame:
    df = pd.DataFrame(vitals)
    if df.empty:
        return df

    df["visit_date"] = pd.to_datetime(df["visit_date"], errors="coerce")
    df["reading"] = pd.to_numeric(df["reading"], errors="coerce")

    return df.dropna(subset=["visit_date", "reading"])

def summarize_vitals(vitals: List[Dict[str, Any]]) -> Dict[str, Any]:
    df = normalize_vitals(vitals)

    if df.empty:
        return {
            "summary": "No recent vital signs available.",
            "details": [],
            "citations": []
        }

    def safe_float(x):
        return float(x) if x is not None else None

    results = []
    citations = []

    for vital_type, group in df.groupby("vital_type"):
        group = group.sort_values("visit_date")

        latest = group.iloc[-1]
        min_val = group["reading"].min()
        max_val = group["reading"].max()

        results.append({
            "vital_type": vital_type,
            "latest_reading": safe_float(latest["reading"]),
            "latest_date": latest["visit_date"].date().isoformat(),
            "min": safe_float(min_val),
            "max": safe_float(max_val),
        })

        citations.append({
            "vital_type": vital_type,
            "date": latest["visit_date"].date().isoformat(),
            "source": "vitals.csv"
        })

    return {
        "summary": f"Reviewed {len(results)} vital sign categories.",
        "details": results,
        "citations": citations
    }


if __name__ == "__main__":
    from backend.data_loader import DataLoader

    loader = DataLoader()
    snap = loader.get_patient_snapshot(1002)

    vitals_summary = summarize_vitals(snap["vitals"])
    print(vitals_summary)
