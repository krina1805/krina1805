# Healthcare Web App (FastAPI Backend)

Ethical healthcare education platform that provides **general health information only**.

## Safety Principles
- No diagnosis, prescriptions, or personalized medical treatment plans.
- Disclaimer included in all API responses.
- Safety filter blocks unsafe/self-harm/prescribing style requests.
- Emergency guidance is included for severe symptoms.

## Backend Structure

```text
/backend
  /app
    /routers
      topics.py
      symptoms.py
      safety.py
      auth.py
    /models
      topic.py
      symptom.py
    /schemas
      topic_schema.py
      symptom_schema.py
    /services
      topic_service.py
      symptom_service.py
      safety_service.py
    /middleware
      safety_middleware.py
      logging_middleware.py
      rate_limit_middleware.py
    /core
      config.py
      database.py
    main.py
```

## API Endpoints
- `GET /api/topics` – general health topics.
- `POST /api/symptoms` – symptom education (non-diagnostic).
- `POST /api/safety/check` – content safety check.
- `GET /api/auth/status` – optional auth placeholder.

## Run Locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Docker

```bash
docker compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`


## Windows Setup Note (pydantic-core / Rust error)

If you see an install failure mentioning `pydantic-core` and Rust/Cargo on Python 3.14, use one of these options:

1. Use Python **3.11-3.13** for this project (recommended).
2. Remove strict `--only-binary=all` pinning and let pip resolve compatible wheels.

Example:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```
