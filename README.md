# Healthcare Web App (Python + HTML + SQL)

Ethical healthcare education platform built with **FastAPI (Python)**, server-rendered **HTML**, and **SQLite SQL** storage.

## Safety Principles
- No diagnosis, prescriptions, or personalized medical treatment plans.
- Disclaimer included in all API responses and home page.
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
  /templates
    index.html
  /sql
    schema.sql
```

## API Endpoints
- `GET /api/topics` – general health topics (from SQL table).
- `POST /api/symptoms` – symptom education (non-diagnostic) and query logging to SQL.
- `POST /api/safety/check` – content safety check.
- `GET /api/auth/status` – optional auth placeholder.
- `GET /` – HTML landing page.

## Run Locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Notes
- Stack is intentionally limited to **Python, HTML, and SQL** for this version.
- SQLite database file (`healthcare.db`) is created automatically on startup.
