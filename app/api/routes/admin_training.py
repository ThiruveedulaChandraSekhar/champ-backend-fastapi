from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.ml.medicine_success_model import train_model as train_medicine_success
from app.ml.recovery_model import train_model as train_recovery
from app.schemas.training import MedicineSuccessTrainingRequest, RecoveryTrainingRequest, TrainingResponse

router = APIRouter(prefix="/api/v1/admin", tags=["admin-training"])


@router.post(
    "/train/medicine-success",
    response_model=TrainingResponse,
    summary="Train the medicine success model",
)
def train_medicine_success_route(payload: MedicineSuccessTrainingRequest):
    try:
        _, _, model_path, preprocessor_path = train_medicine_success([record.model_dump() for record in payload.records])
        return TrainingResponse(
            message="Medicine success model trained successfully.",
            model_path=model_path,
            preprocessor_path=preprocessor_path,
            records_used=len(payload.records),
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post(
    "/train/recovery",
    response_model=TrainingResponse,
    summary="Train the recovery prediction model",
)
def train_recovery_route(payload: RecoveryTrainingRequest):
    try:
        _, _, _, xgb_path, rf_path, preprocessor_path = train_recovery([record.model_dump() for record in payload.records])
        return TrainingResponse(
            message="Recovery model trained successfully.",
            model_path=f"{xgb_path}; {rf_path}",
            preprocessor_path=preprocessor_path,
            records_used=len(payload.records),
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
