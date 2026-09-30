from __future__ import annotations

from typing import Any

from app.ml.drug_allergy_model import DrugAllergyModelUnavailable, predict_drug_allergy


def evaluate_safety(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        return predict_drug_allergy(payload)
    except DrugAllergyModelUnavailable as exc:
        return {
            "safe": None,
            "warning": None,
            "severity": "UNKNOWN",
            "alerts": [],
            "prediction": "UNKNOWN",
            "probability": None,
            "model": "drug-allergy-model",
            "message": f"Drug-allergy model unavailable: {exc}",
        }
