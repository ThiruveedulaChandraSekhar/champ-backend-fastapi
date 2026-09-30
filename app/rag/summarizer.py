from __future__ import annotations

from typing import Any


def summarize_history(patient: dict[str, Any], diagnoses: list[dict[str, Any]], medicines: list[dict[str, Any]], allergies: list[dict[str, Any]], visits: list[dict[str, Any]], retrieved_documents: list[str]) -> str:
    diagnosis_names = [item.get("name") or item.get("diagnosis") for item in diagnoses if item.get("name") or item.get("diagnosis")]
    allergy_names = [item.get("title") for item in allergies if item.get("title")]
    medicine_names = [item.get("name") for item in medicines if item.get("name")]

    parts: list[str] = []
    if diagnosis_names:
        diagnosis_text = ", ".join(diagnosis_names[:3])
        parts.append(f"Patient has a history of {diagnosis_text.lower()}")
    if allergy_names:
        allergy_text = ", ".join(allergy_names[:3])
        parts.append(f"and a recorded {allergy_text.lower()} allergy")
    if medicines:
        latest_medicine = medicines[0]
        medicine_name = latest_medicine.get("name") or "a previous medicine"
        duration = latest_medicine.get("duration")
        outcome = latest_medicine.get("outcome") or "recovery"
        if duration:
            parts.append(f"Previous treatment with {medicine_name} was associated with recovery within approximately {duration} days")
        else:
            parts.append(f"Previous treatment with {medicine_name} was associated with {outcome.lower()} outcome")
    if visits and retrieved_documents:
        latest_visit = visits[0]
        if latest_visit.get("recovery_days"):
            parts.append(f"and prior recovery within about {latest_visit.get('recovery_days')} days")

    summary = ". ".join(parts)
    if not summary:
        return "Patient history is limited or not yet available."
    return summary.strip().capitalize() + "."
