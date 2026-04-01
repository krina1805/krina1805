from app.schemas.symptom_schema import SymptomResponse
from app.services.topic_service import DISCLAIMER


def build_symptom_education(symptoms: list[str]) -> SymptomResponse:
    normalized = [symptom.strip().lower() for symptom in symptoms if symptom.strip()]
    return SymptomResponse(
        symptoms=normalized,
        general_info=(
            "Symptoms can be caused by many conditions. This API provides general education and cannot diagnose."
        ),
        when_to_seek_help=(
            "Seek professional care if symptoms are severe, worsening, or lasting longer than expected."
        ),
        emergency_guidance=(
            "Call emergency services immediately for trouble breathing, chest pain, severe bleeding, "
            "new confusion, or signs of stroke."
        ),
        disclaimer=DISCLAIMER,
    )
