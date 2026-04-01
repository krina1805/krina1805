from app.models.topic import Topic


DISCLAIMER = (
    "This content is educational only and is not a diagnosis or treatment plan. "
    "Always consult a licensed clinician for personal medical concerns."
)


def list_topics() -> list[Topic]:
    return [
        Topic(
            name="Fever",
            info="Fever is often the body's response to infection. Hydration and rest are commonly helpful.",
            disclaimer=DISCLAIMER,
        ),
        Topic(
            name="Hydration",
            info="Adequate fluids support circulation, temperature regulation, and organ function.",
            disclaimer=DISCLAIMER,
        ),
        Topic(
            name="Stress",
            info="Stress can affect sleep, mood, and physical health; habits like exercise and sleep routines can help.",
            disclaimer=DISCLAIMER,
        ),
    ]
