# Healthcare FAQ Chatbot (No JavaScript)

A simple AI-style healthcare chatbot organized inside one folder:

- **HTML** (server-rendered UI)
- **Python + Flask** (backend logic)
- **SQLite/SQL** (FAQ storage)

## Project folder
All chatbot files are in:

`backend/healthcare_chatbot/`

### Contents
- `backend/healthcare_chatbot/app.py` — Flask app, form handling, SQL lookups
- `backend/healthcare_chatbot/templates/healthcare_chatbot.html` — no-JS HTML form UI
- `backend/healthcare_chatbot/sql/healthcare_faqs.sql` — SQL schema + starter FAQ rows
- `backend/healthcare_chatbot/healthcare_faq.db` — created automatically at runtime

## Run locally
```bash
pip install -r backend/requirements.txt
python backend/healthcare_chatbot/app.py
```

Open: `http://localhost:8000`

## Behavior
1. User submits a health question using the HTML form.
2. Python processes the request server-side.
3. The app checks the SQL-backed `healthcare_faqs` table.
4. If no match is found, it advises consulting a healthcare professional.
