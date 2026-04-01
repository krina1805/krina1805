from pathlib import Path
import sqlite3
from flask import Flask, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "healthcare_faq.db"

app = Flask(__name__, template_folder=str(BASE_DIR / "templates"))

DEFAULT_RESPONSE = (
    "I couldn't find a matching answer in our FAQ database. "
    "Please consult a qualified healthcare professional for personalized advice."
)


def initialize_database() -> None:
    """Create the FAQs table and seed starter data if the table is empty."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS healthcare_faqs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            )
            """
        )

        row_count = conn.execute("SELECT COUNT(*) FROM healthcare_faqs").fetchone()[0]
        if row_count == 0:
            conn.executemany(
                "INSERT INTO healthcare_faqs (question, answer) VALUES (?, ?)",
                [
                    (
                        "What are common symptoms of flu?",
                        "Common flu symptoms include fever, cough, sore throat, body aches, fatigue, and chills.",
                    ),
                    (
                        "How much water should I drink daily?",
                        "Many adults benefit from roughly 2 to 3 liters of fluids daily, but needs vary by person and climate.",
                    ),
                    (
                        "How can I improve sleep quality?",
                        "Keep a regular sleep schedule, reduce evening caffeine, avoid heavy meals late, and create a dark, quiet bedroom.",
                    ),
                ],
            )
        conn.commit()


def find_best_answer(user_query: str) -> str:
    """Return the closest FAQ answer based on substring and keyword matching."""
    cleaned_query = user_query.strip().lower()
    if not cleaned_query:
        return "Please enter a health-related question."

    keywords = [word for word in cleaned_query.split() if len(word) > 2]

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        exact_or_substring_match = conn.execute(
            """
            SELECT answer
            FROM healthcare_faqs
            WHERE LOWER(question) LIKE ?
            ORDER BY id ASC
            LIMIT 1
            """,
            (f"%{cleaned_query}%",),
        ).fetchone()
        if exact_or_substring_match:
            return exact_or_substring_match["answer"]

        for keyword in keywords:
            keyword_match = conn.execute(
                """
                SELECT answer
                FROM healthcare_faqs
                WHERE LOWER(question) LIKE ?
                ORDER BY id ASC
                LIMIT 1
                """,
                (f"%{keyword}%",),
            ).fetchone()
            if keyword_match:
                return keyword_match["answer"]

    return DEFAULT_RESPONSE


@app.route("/", methods=["GET", "POST"])
def healthcare_chatbot() -> str:
    user_question = ""
    bot_response = ""

    if request.method == "POST":
        user_question = request.form.get("question", "")
        bot_response = find_best_answer(user_question)

    return render_template(
        "healthcare_chatbot.html",
        user_question=user_question,
        bot_response=bot_response,
    )


initialize_database()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
