from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

Gender = Literal["MALE", "FEMALE", "OTHER", "UNKNOWN"]
Outcome = Literal["EFFECTIVE", "INEFFECTIVE", "UNKNOWN", "RECOVERED"]


class PatientContext(BaseModel):
    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[Gender] = None


class DiagnosisInput(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None


class MedicineHistoryItem(BaseModel):
    name: Optional[str] = None
    active_ingredient: Optional[str] = None
    duration: Optional[int] = Field(None, ge=0)
    outcome: Optional[Outcome] = None


class AllergyHistoryItem(BaseModel):
    title: Optional[str] = None
    severity: Optional[str] = None


class VisitHistoryItem(BaseModel):
    diagnosis: Optional[str] = None
    medicine: Optional[str] = None
    recovery_days: Optional[int] = Field(None, ge=0)
    outcome: Optional[Outcome] = None


class HistorySummaryRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "patient": {"age": 35, "gender": "MALE"},
            "diagnoses": [{"name": "Respiratory Infection", "code": "J06.9"}],
            "medicines": [{"name": "Medicine A", "active_ingredient": "Ingredient A", "duration": 5, "outcome": "EFFECTIVE"}],
            "allergies": [{"title": "Penicillin Allergy", "severity": "HIGH"}],
            "visits": [{"diagnosis": "Respiratory Infection", "medicine": "Medicine A", "recovery_days": 5, "outcome": "RECOVERED"}],
        }
    })

    patient: PatientContext
    diagnoses: list[DiagnosisInput] = Field(default_factory=list)
    medicines: list[MedicineHistoryItem] = Field(default_factory=list)
    allergies: list[AllergyHistoryItem] = Field(default_factory=list)
    visits: list[VisitHistoryItem] = Field(default_factory=list)


class HistorySummaryResponse(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "summary": "Patient has a history of respiratory infections and a recorded penicillin allergy. Previous treatment with medicine a was associated with recovery within approximately 5 days.",
            "evidence": ["Visit: Diagnosis Respiratory Infection; Medicine Medicine A; Recovery 5 days; Outcome Recovered."],
        }
    })

    summary: str
    evidence: list[str] = Field(default_factory=list)
