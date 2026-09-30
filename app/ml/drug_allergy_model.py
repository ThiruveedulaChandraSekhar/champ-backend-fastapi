from __future__ import annotations

from pathlib import Path

from app.config import settings


MODEL_NAME = "drug_allergy_model.pkl"
PREPROCESSOR_NAME = "drug_allergy_preprocessor.pkl"


class DrugAllergyModelUnavailable(RuntimeError):
    pass


def predict_drug_allergy(payload: dict[str, object]) -> dict[str, object]:
    """Run the existing drug-allergy model when its artifacts are installed.

    This repository currently contains no drug-allergy artifact or training feature
    contract. Refusing to guess here is intentional: a medicine-success model or a
    string matcher cannot substitute for the requested safety model.
    """
    model_dir = Path(settings.model_dir)
    model_path = model_dir / MODEL_NAME
    preprocessor_path = model_dir / PREPROCESSOR_NAME
    if not model_path.exists() or not preprocessor_path.exists():
        raise DrugAllergyModelUnavailable(
            f"Missing drug-allergy model artifacts: {MODEL_NAME} and {PREPROCESSOR_NAME}"
        )

    raise DrugAllergyModelUnavailable(
        "Drug-allergy model artifacts were found, but their training feature contract is not declared."
    )