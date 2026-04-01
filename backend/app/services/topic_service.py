from app.core.database import get_connection, seed_topics
from app.models.topic import Topic


DISCLAIMER = (
    "This content is educational only and is not a diagnosis or treatment plan. "
    "Always consult a licensed clinician for personal medical concerns."
)

DEFAULT_TOPICS = [
    (
        "Fever",
        "Fever is often the body's response to infection. Hydration and rest are commonly helpful.",
        DISCLAIMER,
    ),
    (
        "Hydration",
        "Adequate fluids support circulation, temperature regulation, and organ function.",
        DISCLAIMER,
    ),
    (
        "Stress",
        "Stress can affect sleep, mood, and physical health; habits like exercise and sleep routines can help.",
        DISCLAIMER,
    ),
]


def bootstrap_topics() -> None:
    seed_topics(DEFAULT_TOPICS)


def list_topics() -> list[Topic]:
    with get_connection() as conn:
        rows = conn.execute("SELECT name, info, disclaimer FROM topics ORDER BY name").fetchall()
    return [Topic(**dict(row)) for row in rows]
