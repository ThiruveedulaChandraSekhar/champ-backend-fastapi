from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "Medical AI Service"
    app_version: str = "1.0.0"
    environment: str = "development"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:8080"
    model_dir: str = str(BASE_DIR / "app" / "trained_models")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        protected_namespaces=(),
    )


settings = Settings()
