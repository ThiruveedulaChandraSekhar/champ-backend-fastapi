from __future__ import annotations

from typing import Any


def build_document_from_history(history_payload: dict[str, Any]) -> list[str]:
    documents: list[str] = []
    for visit in history_payload.get("previous_visits", []) or []:
        diagnosis = visit.get("diagnosis") or "Unknown diagnosis"
        medicine = visit.get("medicine") or "Unknown medicine"
        recovery_days = visit.get("recovery_days")
        outcome = visit.get("outcome") or "Unknown outcome"
        documents.append(
            f"Visit: Diagnosis {diagnosis}; Medicine {medicine}; Recovery {recovery_days} days; Outcome {outcome}."
        )

    for treatment in history_payload.get("previous_treatments", []) or []:
        diagnosis = treatment.get("diagnosis") or "Unknown diagnosis"
        recovery_days = treatment.get("recovery_days")
        outcome = treatment.get("outcome") or "Unknown outcome"
        documents.append(
            f"Previous treatment: {diagnosis}; Recovery {recovery_days} days; Outcome {outcome}."
        )

    for med in history_payload.get("previous_medicines", []) or []:
        name = med.get("medicine") or "Unknown medicine"
        ingredient = med.get("active_ingredient") or "unknown ingredient"
        outcome = med.get("outcome") or "Unknown outcome"
        documents.append(f"Medication history: {name} ({ingredient}); Outcome {outcome}.")

    return documents
