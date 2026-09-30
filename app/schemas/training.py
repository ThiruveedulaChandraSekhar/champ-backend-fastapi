from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

Gender = Literal["MALE", "FEMALE", "OTHER", "UNKNOWN"]


class MedicineSuccessTrainingRecord(BaseModel):
    model_config = {"protected_namespaces": ()}

    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[Gender] = None
    diagnosis: Optional[str] = None
    diagnosis_code: Optional[str] = None
    medicine: Optional[str] = None
    active_ingredient: Optional[str] = None
    dosage: Optional[str] = None
    duration: Optional[int] = Field(None, ge=0)
    previous_recovery_days: Optional[int] = Field(None, ge=0)
    previous_treatment_success: Optional[int] = Field(None, ge=0, le=1)
    medicine_success: Optional[int] = Field(None, ge=0, le=1)


class RecoveryTrainingRecord(BaseModel):
    model_config = {"protected_namespaces": ()}

    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[Gender] = None
    diagnosis: Optional[str] = None
    diagnosis_code: Optional[str] = None
    medicine: Optional[str] = None
    active_ingredient: Optional[str] = None
    dosage: Optional[str] = None
    duration: Optional[int] = Field(None, ge=0)
    previous_recovery_days: Optional[int] = Field(None, ge=0)
    previous_visit_count: Optional[int] = Field(None, ge=0)
    previous_treatment_success: Optional[int] = Field(None, ge=0, le=1)
    recovery_days: Optional[int] = Field(None, ge=0)


class MedicineSuccessTrainingRequest(BaseModel):
    records: list[MedicineSuccessTrainingRecord]


class RecoveryTrainingRequest(BaseModel):
    records: list[RecoveryTrainingRecord]


class TrainingResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    message: str
    model_path: str
    preprocessor_path: str
    records_used: int
