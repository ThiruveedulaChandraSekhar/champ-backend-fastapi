from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from xgboost import XGBClassifier

from app.config import settings
from app.ml.preprocessing import build_preprocessor, prepare_training_frame, save_preprocessor


MODEL_NAME = "medicine_success_xgb.pkl"
PREPROCESSOR_NAME = "medicine_success_preprocessor.pkl"


def train_model(records: list[dict[str, Any]]) -> tuple[XGBClassifier, Any, str, str]:
    X, y = prepare_training_frame(records, "medicine_success")
    if y.nunique() < 2:
        raise ValueError("Medicine success training target must contain both positive and negative examples to train a binary classifier.")
    preprocessor = build_preprocessor(X)
    transformed = preprocessor.fit_transform(X)
    model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        objective="binary:logistic",
        random_state=42,
        eval_metric="logloss",
    )
    model.fit(transformed, y)

    model_dir = Path(settings.model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = str(model_dir / MODEL_NAME)
    preprocessor_path = str(model_dir / PREPROCESSOR_NAME)
    joblib.dump(model, model_path)
    save_preprocessor(preprocessor, preprocessor_path)
    return model, preprocessor, model_path, preprocessor_path


def load_model() -> tuple[XGBClassifier, Any]:
    model_dir = Path(settings.model_dir)
    model = joblib.load(model_dir / MODEL_NAME)
    preprocessor = joblib.load(model_dir / PREPROCESSOR_NAME)
    return model, preprocessor


def predict_success(payload: dict[str, Any]) -> float:
    model, preprocessor = load_model()
    row = pd.DataFrame([payload])
    transformed = preprocessor.transform(row)
    probability = model.predict_proba(transformed)[0][1]
    return float(probability)
