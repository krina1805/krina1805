UNSAFE_KEYWORDS = {
    "suicide",
    "self-harm",
    "kill",
    "overdose",
    "prescribe",
    "dosage for me",
}


def is_unsafe_text(text: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in UNSAFE_KEYWORDS)
