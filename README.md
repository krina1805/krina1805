# Healthcare FAQ Chatbot (No JavaScript)

This repository now includes a simple AI-style healthcare chatbot that uses:
- **HTML** (server-rendered UI)
- **Python + Flask** (backend logic)
- **SQLite/SQL** (healthcare FAQ storage)

## Files
- `backend/healthcare_chatbot_app.py` — Flask app, form handling, SQL lookups
- `backend/templates/healthcare_chatbot.html` — HTML UI with plain form submission (no JS)
- `backend/sql/healthcare_faqs.sql` — SQL schema + starter FAQ rows

## Run locally
```bash
pip install -r backend/requirements.txt
python backend/healthcare_chatbot_app.py
```

Then open: `http://localhost:8000`

## Behavior
1. User submits a health question from an HTML form.
2. Python processes the question.
3. The app searches `healthcare_faqs` in SQLite for a relevant answer.
4. If nothing matches, it returns:
   "Please consult a qualified healthcare professional for personalized advice."
