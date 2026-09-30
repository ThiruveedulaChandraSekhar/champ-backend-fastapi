from __future__ import annotations

from typing import Any

from app.ml.recovery_model import predict_recovery


def predict_recovery_time(payload: dict[str, Any]) -> dict[str, Any]:
    return predict_recovery(payload)
