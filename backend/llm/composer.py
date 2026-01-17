from typing import Dict, Any

def compose_context(snapshot: Dict[str, Any],
                    vitals: Dict[str, Any],
                    oasis: Dict[str, Any],
                    diagnoses: Dict[str, Any],
                    wounds: Dict[str, Any],
                    medications: Dict[str, Any]) -> Dict[str, Any]:

    return {
        "patient_id": snapshot["patient_id"],
        "episode_id": snapshot["episode_id"],
        "diagnoses": diagnoses,
        "functional_status": oasis,
        "vitals": vitals,
        "wounds": wounds,
        "medications": medications
    }
