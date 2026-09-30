from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.schemas.history import HistorySummaryRequest, HistorySummaryResponse
from app.services.history_service import summarize_patient_history

router = APIRouter(prefix="/api/v1", tags=["history"])


@router.post(
    "/history/summary",
    response_model=HistorySummaryResponse,
    summary="Generate a concise medical history summary",
    description="Creates a compact summary from patient history JSON supplied by Spring Boot, using in-memory documents for retrieval before synthesis.",
)
def summarize_history_route(payload: HistorySummaryRequest):
    try:
        result = summarize_patient_history(payload.model_dump())
        return result
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
