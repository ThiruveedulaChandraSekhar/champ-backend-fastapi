from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.schemas.prediction import MedicineSuccessRequest, MedicineSuccessResponse
from app.services.medicine_success_service import predict_medicine_success

router = APIRouter(prefix="/api/v1", tags=["medicine-success"])


@router.post(
    "/predictions/medicine-success",
    response_model=MedicineSuccessResponse,
    summary="Predict whether treatment is likely to be effective",
    description="Receives patient and treatment information from Spring Boot and returns a probability and classification.",
    responses={
        200: {"description": "Prediction generated successfully."},
        400: {"description": "Invalid request payload."},
    },
)
def predict_success_route(payload: MedicineSuccessRequest):
    try:
        result = predict_medicine_success({
            "age": payload.patient.age,
            "gender": payload.patient.gender,
            "diagnosis": payload.current_treatment.diagnosis,
            "diagnosis_code": payload.current_treatment.diagnosis_code,
            "medicine": payload.current_treatment.medicine,
            "active_ingredient": payload.current_treatment.active_ingredient,
            "dosage": payload.current_treatment.dosage,
            "duration": payload.current_treatment.duration,
            "previous_recovery_days": (payload.history.previous_treatments[0].recovery_days if payload.history.previous_treatments else None),
            "previous_treatment_success": 1 if any(item.outcome == "EFFECTIVE" for item in payload.history.previous_treatments) else 0,
        })
        return result
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
