from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

AlertSeverity = Literal["UNKNOWN", "NO_RECORDED_CONFLICT", "LOW_RISK", "MEDIUM_RISK", "HIGH_RISK"]


class SafetyCheckRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore", json_schema_extra={
        "example": {
            "medicineName": "Amoxicillin",
            "activeIngredient": "amoxicillin",
            "patientDrugAllergies": ["Penicillin"],
        }
    })

    medicine_name: str = Field(alias="medicineName", min_length=1)
    active_ingredient: Optional[str] = Field(default=None, alias="activeIngredient")
    patient_drug_allergies: list[str] = Field(default_factory=list, alias="patientDrugAllergies")


class SafetyAlert(BaseModel):
    reason: str
    medicine: Optional[str] = None
    allergy: Optional[str] = None


class SafetyCheckResponse(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "safe": None,
            "warning": None,
            "severity": "UNKNOWN",
            "alerts": [],
            "prediction": "UNKNOWN",
            "probability": None,
            "model": "drug-allergy-model",
            "message": "Drug-allergy model is unavailable; no clinical conclusion was made.",
        }
    })

    safe: Optional[bool] = None
    warning: Optional[bool] = None
    severity: AlertSeverity = "UNKNOWN"
    alerts: list[SafetyAlert] = Field(default_factory=list)
    prediction: Optional[str] = None
    probability: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    model: Optional[str] = None
    message: Optional[str] = None
