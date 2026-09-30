from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes.admin_training import router as training_router
from app.api.routes.history import router as history_router
from app.api.routes.medicine_success import router as medicine_success_router
from app.api.routes.recovery import router as recovery_router
from app.api.routes.safety import router as safety_router
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Medical AI/ML service for Spring Boot integration. This service does not access PostgreSQL or any backend database.",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/api/v1/health", tags=["health"])
def health_check():
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "database_access": "not_used",
    }


@app.get("/api/v1/models/status", tags=["models"])
def model_status():
    model_dir = Path(settings.model_dir)
    expected = {
        "medicine_success_xgb.pkl": model_dir / "medicine_success_xgb.pkl",
        "medicine_success_preprocessor.pkl": model_dir / "medicine_success_preprocessor.pkl",
        "recovery_xgb.pkl": model_dir / "recovery_xgb.pkl",
        "recovery_rf.pkl": model_dir / "recovery_rf.pkl",
        "recovery_preprocessor.pkl": model_dir / "recovery_preprocessor.pkl",
        "drug_allergy_model.pkl": model_dir / "drug_allergy_model.pkl",
        "drug_allergy_preprocessor.pkl": model_dir / "drug_allergy_preprocessor.pkl",
    }
    available = {name: "available" if path.exists() else "missing" for name, path in expected.items()}
    return {
        "status": "ready" if all(value == "available" for value in available.values()) else "partial",
        "models": available,
    }


app.include_router(medicine_success_router)
app.include_router(recovery_router)
app.include_router(safety_router)
app.include_router(history_router)
app.include_router(training_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
