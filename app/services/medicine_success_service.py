from __future__ import annotations

from typing import Any

from app.ml.medicine_success_model import predict_success


def predict_medicine_success(payload: dict[str, Any]) -> dict[str, Any]:
    probability = predict_success(payload)
    prediction = "Likely Effective" if probability >= 0.6 else "Needs Review"
    return {
        "success_probability": round(float(probability), 4),
        "prediction": prediction,
        "model": "XGBoost",
        "model_version": "1.0.0",
    }
