from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field, ConfigDict


Gender = Literal["MALE", "FEMALE", "OTHER", "UNKNOWN"]
Outcome = Literal["EFFECTIVE", "INEFFECTIVE", "UNKNOWN", "RECOVERED"]


class PatientSummary(BaseModel):
    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[Gender] = None


class CurrentTreatment(BaseModel):
    diagnosis: str = Field(..., description="Current diagnosis name")
    diagnosis_code: Optional[str] = None
    medicine: str = Field(..., description="Medicine currently prescribed")
    active_ingredient: str = Field(..., description="Active ingredient")
    dosage: Optional[str] = None
    duration: Optional[int] = Field(None, ge=0)


class PreviousMedicine(BaseModel):
    medicine: Optional[str] = None
    active_ingredient: Optional[str] = None
    dosage: Optional[str] = None
    duration: Optional[int] = Field(None, ge=0)
    outcome: Optional[Outcome] = None


class PreviousTreatment(BaseModel):
    diagnosis: Optional[str] = None
    recovery_days: Optional[int] = Field(None, ge=0)
    outcome: Optional[Outcome] = None


class HistoryPayload(BaseModel):
    previous_medicines: list[PreviousMedicine] = Field(default_factory=list)
    previous_treatments: list[PreviousTreatment] = Field(default_factory=list)
    previous_visits: list["PreviousVisit"] = Field(default_factory=list)


class PreviousVisit(BaseModel):
    diagnosis: Optional[str] = None
    medicine: Optional[str] = None
    recovery_days: Optional[int] = Field(None, ge=0)
    outcome: Optional[Outcome] = None


class MedicineSuccessRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "patient": {"age": 35, "gender": "MALE"},
            "current_treatment": {
                "diagnosis": "Respiratory Infection",
                "diagnosis_code": "J06.9",
                "medicine": "Example Medicine",
                "active_ingredient": "Example Ingredient",
                "dosage": "500 mg",
                "duration": 5,
            },
            "history": {
                "previous_medicines": [{
                    "medicine": "Medicine A",
                    "active_ingredient": "Ingredient A",
                    "dosage": "250 mg",
                    "duration": 5,
                    "outcome": "EFFECTIVE",
                }],
                "previous_treatments": [{
                    "diagnosis": "Previous Infection",
                    "recovery_days": 4,
                    "outcome": "EFFECTIVE",
                }],
            },
        }
    })

    patient: PatientSummary
    current_treatment: CurrentTreatment
    history: HistoryPayload = Field(default_factory=HistoryPayload)


class RecoveryTimeRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "patient": {"age": 35, "gender": "MALE"},
            "current_treatment": {
                "diagnosis": "Respiratory Infection",
                "diagnosis_code": "J06.9",
                "medicine": "Example Medicine",
                "active_ingredient": "Example Ingredient",
                "dosage": "500 mg",
                "duration": 5,
            },
            "history": {
                "previous_visits": [{
                    "diagnosis": "Fever",
                    "medicine": "Medicine A",
                    "recovery_days": 4,
                }, {
                    "diagnosis": "Respiratory Infection",
                    "medicine": "Medicine B",
                    "recovery_days": 6,
                }],
            },
        }
    })

    patient: PatientSummary
    current_treatment: CurrentTreatment
    history: HistoryPayload = Field(default_factory=HistoryPayload)


class MedicineSuccessResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success_probability": 0.85,
                "prediction": "Likely Effective",
                "model": "XGBoost",
                "model_version": "1.0.0",
            }
        },
        protected_namespaces=(),
    )

    success_probability: float = Field(..., ge=0.0, le=1.0)
    prediction: str
    model: str = "XGBoost"
    model_version: str = "1.0.0"


class RecoveryRange(BaseModel):
    minimum_days: int
    maximum_days: int


class RecoveryTimeResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "estimated_recovery_days": 5.0,
                "estimated_range": {"minimum_days": 3, "maximum_days": 7},
                "model": "XGBoost",
                "model_version": "1.0.0",
            }
        },
        protected_namespaces=(),
    )

    estimated_recovery_days: float
    estimated_range: RecoveryRange
    model: str = "XGBoost"
    model_version: str = "1.0.0"


class ModelStatusResponse(BaseModel):
    status: str
    models: dict[str, str]
