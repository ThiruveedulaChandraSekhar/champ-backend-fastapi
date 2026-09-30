from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


CATEGORICAL_COLUMNS = [
    "diagnosis",
    "diagnosis_code",
    "medicine",
    "active_ingredient",
    "dosage",
    "gender",
]

NUMERICAL_COLUMNS = [
    "age",
    "duration",
    "previous_recovery_days",
    "previous_visit_count",
    "previous_treatment_success",
]


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    numeric_cols = [col for col in NUMERICAL_COLUMNS if col in X.columns]
    categorical_cols = [col for col in CATEGORICAL_COLUMNS if col in X.columns]

    numerical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])

    transformers = []
    if numeric_cols:
        transformers.append(("num", numerical_transformer, numeric_cols))
    if categorical_cols:
        transformers.append(("cat", categorical_transformer, categorical_cols))

    return ColumnTransformer(transformers=transformers, remainder="drop")


def prepare_training_frame(records: list[dict[str, Any]], target_name: str) -> tuple[pd.DataFrame, pd.Series]:
    df = pd.DataFrame(records)
    if df.empty:
        raise ValueError("Training data is empty.")
    if target_name not in df.columns:
        raise ValueError(f"Target column '{target_name}' missing from training data.")
    feature_columns = [c for c in df.columns if c != target_name]
    return df[feature_columns], df[target_name]


def save_preprocessor(preprocessor: ColumnTransformer, path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(preprocessor, path)


def load_preprocessor(path: str) -> ColumnTransformer:
    return joblib.load(path)
