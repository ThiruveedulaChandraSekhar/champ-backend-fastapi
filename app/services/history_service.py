from __future__ import annotations

from typing import Any

from app.rag.document_builder import build_document_from_history
from app.rag.retriever import retrieve_relevant_documents
from app.rag.summarizer import summarize_history


def summarize_patient_history(payload: dict[str, Any]) -> dict[str, Any]:
    patient = payload.get("patient", {})
    diagnoses = payload.get("diagnoses", [])
    medicines = payload.get("medicines", [])
    allergies = payload.get("allergies", [])
    visits = payload.get("visits", [])
    history_payload = {
        "previous_visits": visits,
        "previous_treatments": [{
            "diagnosis": visit.get("diagnosis"),
            "recovery_days": visit.get("recovery_days"),
            "outcome": visit.get("outcome"),
        } for visit in visits],
        "previous_medicines": medicines,
    }
    documents = build_document_from_history(history_payload)
    query = " ".join([str(item.get("name") or item.get("diagnosis") or "") for item in diagnoses + medicines + allergies])
    retrieved_documents = retrieve_relevant_documents(documents, query, top_k=3)
    summary = summarize_history(patient, diagnoses, medicines, allergies, visits, retrieved_documents)
    return {
        "summary": summary,
        "evidence": retrieved_documents,
    }
