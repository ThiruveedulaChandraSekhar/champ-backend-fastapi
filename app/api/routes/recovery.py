from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.schemas.prediction import RecoveryTimeRequest, RecoveryTimeResponse
from app.services.recovery_service import predict_recovery_time

router = APIRouter(prefix="/api/v1", tags=["recovery"])


@router.post(
    "/predictions/recovery-time",
    response_model=RecoveryTimeResponse,
    summary="Predict approximate recovery time",
    description="Uses historical and current treatment data to estimate recovery duration; output is approximate and not guaranteed.",
)
def predict_recovery_route(payload: RecoveryTimeRequest):
    try:
        result = predict_recovery_time({
            "age": payload.patient.age,
            "gender": payload.patient.gender,
            "diagnosis": payload.current_treatment.diagnosis,
            "diagnosis_code": payload.current_treatment.diagnosis_code,
            "medicine": payload.current_treatment.medicine,
            "active_ingredient": payload.current_treatment.active_ingredient,
            "dosage": payload.current_treatment.dosage,
            "duration": payload.current_treatment.duration,
            "previous_recovery_days": max(
                [visit.recovery_days for visit in payload.history.previous_visits if visit.recovery_days is not None],
                default=0,
            ),
            "previous_visit_count": len(payload.history.previous_visits),
            "previous_treatment_success": 1 if any(item.outcome == "EFFECTIVE" for item in payload.history.previous_treatments) else 0,
        })
        return result
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
