from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class DrugAllergyRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    medicine_name: str = Field(alias="medicineName", min_length=1)
    patient_allergies: list[str] | None = Field(default=None, alias="patientAllergies")


class KnownReaction(BaseModel):
    reaction: str
    hypersensitivity_type: str = Field(alias="hypersensitivityType")
    severity: str

    model_config = ConfigDict(populate_by_name=True)


class DrugAllergyResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    medicine_name: str = Field(alias="medicineName")
    matched: bool
    is_allergic_risk: bool | None = Field(alias="isAllergicRisk")
    risk_level: Literal["LOW", "MODERATE", "HIGH", "UNKNOWN"] = Field(alias="riskLevel")
    reactions: list[KnownReaction]
    patient_allergy_conflict: bool | None = Field(default=None, alias="patientAllergyConflict")
    message: str | None = None
    source: str = "drug_allergy_dataset"