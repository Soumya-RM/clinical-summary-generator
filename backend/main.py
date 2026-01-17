from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.data_loader import DataLoader
from backend.summarizers.vitals import summarize_vitals
from backend.summarizers.oasis import summarize_oasis
from backend.summarizers.diagnoses import summarize_diagnoses
from backend.summarizers.wounds import summarize_wounds
from backend.summarizers.medications import summarize_medications
from backend.llm.composer import compose_context
from backend.llm.client import generate_summary

app = FastAPI(
    title="Clinical Summary Generator API",
    description="Generate structured clinical summaries from EHR data",
    version="1.0.0"
)

# -----------------------------
# Request Schema
# -----------------------------
class SummaryRequest(BaseModel):
    patient_id: int


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}


# -----------------------------
# Core Endpoint
# -----------------------------
@app.post("/generate_summary")
def generate_clinical_summary(request: SummaryRequest):
    loader = DataLoader()

    try:
        snapshot = loader.get_patient_snapshot(request.patient_id)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail=f"Patient {request.patient_id} not found"
        )

    context = compose_context(
        snapshot=snapshot,
        vitals=summarize_vitals(snapshot["vitals"]),
        oasis=summarize_oasis(snapshot["oasis"]),
        diagnoses=summarize_diagnoses(snapshot["diagnoses"]),
        wounds=summarize_wounds(snapshot["wounds"]),
        medications=summarize_medications(snapshot["medications"]),
    )

    try:
        summary = generate_summary(context)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return summary
