from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.schemas.safety import SafetyCheckRequest, SafetyCheckResponse
from app.services.safety_service import evaluate_safety

router = APIRouter(prefix="/api/v1", tags=["safety"])


@router.post(
    "/safety/check",
    response_model=SafetyCheckResponse,
    summary="Check for medicine allergy or conflict risk",
    description="Runs the trained drug-allergy model using structured medicine data and DRUG allergies only.",
)
def check_safety_route(payload: SafetyCheckRequest):
    try:
        result = evaluate_safety(payload.model_dump())
        return result
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
