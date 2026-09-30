from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

from app.config import settings
from app.ml.preprocessing import build_preprocessor, prepare_training_frame, save_preprocessor


XGB_MODEL_NAME = "recovery_xgb.pkl"
RF_MODEL_NAME = "recovery_rf.pkl"
PREPROCESSOR_NAME = "recovery_preprocessor.pkl"


def train_model(records: list[dict[str, Any]]) -> tuple[XGBRegressor, RandomForestRegressor, Any, str, str, str]:
    X, y = prepare_training_frame(records, "recovery_days")
    if y.empty or y.nunique() <= 1:
        raise ValueError("Recovery training target must contain more than one distinct recovery day value.")
    preprocessor = build_preprocessor(X)
    X_transformed = preprocessor.fit_transform(X)

    xgb_model = XGBRegressor(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=42,
    )
    rf_model = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
    )

    xgb_model.fit(X_transformed, y)
    rf_model.fit(X_transformed, y)

    model_dir = Path(settings.model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)
    xgb_path = str(model_dir / XGB_MODEL_NAME)
    rf_path = str(model_dir / RF_MODEL_NAME)
    preprocessor_path = str(model_dir / PREPROCESSOR_NAME)

    joblib.dump(xgb_model, xgb_path)
    joblib.dump(rf_model, rf_path)
    save_preprocessor(preprocessor, preprocessor_path)
    return xgb_model, rf_model, preprocessor, xgb_path, rf_path, preprocessor_path


def load_model() -> tuple[XGBRegressor, RandomForestRegressor, Any]:
    model_dir = Path(settings.model_dir)
    xgb_model = joblib.load(model_dir / XGB_MODEL_NAME)
    rf_model = joblib.load(model_dir / RF_MODEL_NAME)
    preprocessor = joblib.load(model_dir / PREPROCESSOR_NAME)
    return xgb_model, rf_model, preprocessor


def predict_recovery(payload: dict[str, Any]) -> dict[str, Any]:
    xgb_model, rf_model, preprocessor = load_model()
    row = pd.DataFrame([payload])
    transformed = preprocessor.transform(row)
    xgb_pred = float(xgb_model.predict(transformed)[0])
    rf_pred = float(rf_model.predict(transformed)[0])
    prediction = max(0.0, min(xgb_pred, rf_pred))
    variation = max(1.0, abs(xgb_pred - rf_pred) * 0.5)
    minimum = max(0, int(round(prediction - variation)))
    maximum = max(minimum + 1, int(round(prediction + variation)))
    return {
        "estimated_recovery_days": float(round(prediction, 2)),
        "estimated_range": {"minimum_days": minimum, "maximum_days": maximum},
        "model": "XGBoost",
        "model_version": "1.0.0",
    }
