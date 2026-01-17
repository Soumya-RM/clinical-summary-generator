from typing import List, Dict, Any

def summarize_diagnoses(diagnoses: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not diagnoses:
        return {
            "primary_diagnosis": None,
            "comorbidities": [],
            "citations": []
        }

    seen = {}
    for d in diagnoses:
        key = (
            d.get("diagnosis_code"),
            d.get("diagnosis_description")
        )
        if key not in seen:
            seen[key] = d

    unique_diagnoses = list(seen.values())

    primary = unique_diagnoses[0]
    comorbidities = unique_diagnoses[1:]

    return {
        "primary_diagnosis": {
            "description": primary.get("diagnosis_description"),
            "code": primary.get("diagnosis_code")
        },
        "comorbidities": [
            {
                "description": d.get("diagnosis_description"),
                "code": d.get("diagnosis_code")
            }
            for d in comorbidities
        ],
        "citations": [
            {
                "source": "diagnoses.csv",
                "note": "Diagnoses deduplicated per episode"
            }
        ]
    }


if __name__ == "__main__":
    from backend.data_loader import DataLoader

    loader = DataLoader()
    snap = loader.get_patient_snapshot(1002)

    dx_summary = summarize_diagnoses(snap["diagnoses"])
    print(dx_summary)
