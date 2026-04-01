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
