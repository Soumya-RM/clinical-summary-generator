from typing import List, Dict, Any
from collections import Counter

def summarize_medications(medications: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not medications:
        return {
            "summary": "No active medications documented.",
            "details": [],
            "citations": []
        }

    # Deduplicated by medication name
    unique = {}
    for m in medications:
        name = m.get("medication_name")
        if name and name not in unique:
            unique[name] = m

    unique_meds = list(unique.values())

    # Counted classes based on unique meds
    class_counts = Counter(
        m.get("classification")
        for m in unique_meds
        if m.get("classification")
    )

    polypharmacy = len(unique_meds) >= 5

    details = [
        {
            "medication": m.get("medication_name"),
            "frequency": m.get("frequency"),
            "class": m.get("classification")
        }
        for m in unique_meds
    ]

    citations = [
        {
            "medication": m.get("medication_name"),
            "source": "medications.csv"
        }
        for m in unique_meds
    ]

    summary_parts = [
        f"Patient is prescribed {len(unique_meds)} unique active medications."
    ]

    if polypharmacy:
        summary_parts.append("This meets criteria for polypharmacy.")

    if class_counts:
        class_summary = ", ".join(
            f"{count} {cls}" for cls, count in class_counts.items()
        )
        summary_parts.append(f"Medication classes include: {class_summary}.")

    return {
        "summary": " ".join(summary_parts),
        "details": details,
        "citations": citations
    }


if __name__ == "__main__":
    from backend.data_loader import DataLoader

    loader = DataLoader()
    snap = loader.get_patient_snapshot(1002)

    meds_summary = summarize_medications(snap["medications"])
    print(meds_summary)
