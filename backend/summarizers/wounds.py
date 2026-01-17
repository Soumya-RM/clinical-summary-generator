from typing import List, Dict, Any
from collections import Counter

def summarize_wounds(wounds: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not wounds:
        return {
            "summary": "No active wounds documented.",
            "details": [],
            "citations": []
        }

    # Deduplicated wounds by (location, description)
    unique = {}
    for w in wounds:
        key = (w.get("location"), w.get("description"))
        if key not in unique:
            unique[key] = w

    unique_wounds = list(unique.values())

    # Extracted stages
    stages = []
    for w in unique_wounds:
        desc = (w.get("description") or "").upper()
        for stage in ["STAGE IV", "STAGE III", "STAGE II", "STAGE I"]:
            if stage in desc:
                stages.append(stage)
                break

    stage_counts = Counter(stages)
    highest_stage = max(stage_counts.keys(), default=None)

    details = [
        {
            "location": w.get("location"),
            "description": w.get("description")
        }
        for w in unique_wounds
    ]

    citations = [
        {
            "location": w.get("location"),
            "source": "wounds.csv"
        }
        for w in unique_wounds
    ]

    summary_parts = [
        f"Patient has {len(unique_wounds)} distinct documented wounds."
    ]

    if stage_counts:
        stage_summary = ", ".join(
            f"{count} {stage}" for stage, count in stage_counts.items()
        )
        summary_parts.append(f"Wound staging includes: {stage_summary}.")

    if highest_stage:
        summary_parts.append(f"Highest severity noted: {highest_stage}.")

    return {
        "summary": " ".join(summary_parts),
        "details": details,
        "citations": citations
    }


if __name__ == "__main__":
    from backend.data_loader import DataLoader

    loader = DataLoader()
    snap = loader.get_patient_snapshot(1002)

    wounds_summary = summarize_wounds(snap["wounds"])
    print(wounds_summary)
