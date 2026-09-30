# Medical AI FastAPI Service

This project is a standalone AI/ML service for a Spring Boot-based medical application. It accepts JSON payloads from Spring Boot, performs inference, safety checks, history summarization, and training, and returns results without accessing any database or patient records directly.

## Architecture boundary

- PostgreSQL: Spring Boot only
- Spring Boot backend: owns all patient retrieval and auth workflows
- FastAPI AI service: receives JSON from Spring Boot, runs model logic, and returns AI output
- No SQLAlchemy
- No database credentials in FastAPI
- No direct DB access in this service

## Core endpoints

- GET /api/v1/health
- GET /api/v1/models/status
- POST /api/v1/predictions/medicine-success
- POST /api/v1/predictions/recovery-time
- POST /api/v1/safety/check
- POST /api/v1/safety/check
- POST /api/v1/history/summary
- POST /api/v1/admin/train/medicine-success
- POST /api/v1/admin/train/recovery

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected response when the trained artifact is installed:

```json
{
	"safe": false,
	"warning": true,
	"severity": "HIGH_RISK",
	"alerts": [
		{
			"reason": "Potential drug-allergy conflict",
			"medicine": "Amoxicillin",
			"allergy": "Penicillin Allergy"
		}
	],
	"prediction": "Potential Allergy Risk",
	"probability": 0.91,
	"model": "drug-allergy-model",
	"message": "The ML model detected a potential drug-allergy conflict."
}
```

Until the compatible model and its training preprocessor are supplied, the response is `safe: null`, `prediction: "UNKNOWN"`, and contains no fabricated allergy decision.

Then open:

- http://localhost:8000/docs

## Drug allergy model integration

The safety endpoint receives only structured medicine data and allergies already classified as `DRUG` by Spring Boot. It does not read `reason`, diagnosis, recovery, or free-text allergy descriptions. FastAPI does not connect to PostgreSQL or any other database.

The repository currently has no drug-allergy model artifact or declared training feature contract. Until the trained artifact and its exact preprocessing contract are supplied, the endpoint returns `UNKNOWN` rather than using the medicine-success model or inventing a rule-based result.

```powershell
Invoke-RestMethod `
	-Method Post `
	-Uri http://localhost:8000/api/v1/safety/check `
	-ContentType "application/json" `
	-Body '{"medicineName":"Amoxicillin","activeIngredient":"amoxicillin","patientDrugAllergies":["Penicillin"]}'
```
