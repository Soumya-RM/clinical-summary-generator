from typing import List, Dict, Any
import pandas as pd

ADL_SCALE = {
    0: "Independent",
    1: "Requires supervision",
    2: "Requires limited assistance",
    3: "Requires extensive assistance",
    4: "Totally dependent",
    5: "Chairfast / unable to ambulate",
    6: "Totally dependent"
}


def extract_score(value: str):
    """
    Extract numeric OASIS score from strings like:
    '5 - CHAIRFAST, UNABLE TO AMBULATE...'
    """
    if not isinstance(value, str):
        return None
    try:
        return int(value.split(" - ")[0].strip())
    except Exception:
        return None

def summarize_oasis(oasis: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not oasis:
        return {
            "summary": "No OASIS functional assessment available.",
            "details": [],
            "citations": []
        }

    df = pd.DataFrame(oasis)

    # Sorted by assessment date and take latest
    if "assessment_date" in df.columns:
        df["assessment_date"] = pd.to_datetime(df["assessment_date"], errors="coerce")
        df = df.sort_values("assessment_date")

    latest = df.iloc[-1]

    ignore_cols = {"patient_id", "assessment_date", "assessment_type"}
    adl_cols = [c for c in df.columns if c not in ignore_cols]

    details = []
    citations = []
    dependent_count = 0

    for adl in adl_cols:
        raw_value = latest.get(adl)
        score = extract_score(raw_value)

        if score is None:
            continue

        interpretation = ADL_SCALE.get(score, "Unknown")

        if score >= 3:
            dependent_count += 1

        details.append({
            "activity": adl,
            "score": score,
            "interpretation": interpretation,
            "raw_text": raw_value
        })

        citations.append({
            "activity": adl,
            "assessment_date": latest.get("assessment_date"),
            "source": "oasis.csv"
        })

    if not details:
        overall = "Functional status data present but could not be interpreted."
    elif dependent_count == 0:
        overall = "Patient is largely independent in activities of daily living."
    elif dependent_count <= 2:
        overall = "Patient requires assistance with some activities of daily living."
    else:
        overall = "Patient has significant functional limitations and requires substantial assistance."

    return {
        "summary": overall,
        "details": details,
        "citations": citations
    }





if __name__ == "__main__":
    from backend.data_loader import DataLoader

    loader = DataLoader()
    snap = loader.get_patient_snapshot(1002)

    oasis_summary = summarize_oasis(snap["oasis"])
    print(oasis_summary)


