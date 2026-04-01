from pydantic import BaseModel


class SymptomEducation(BaseModel):
    symptom: str
    overview: str
    self_care: list[str]
    when_to_seek_care: str
    emergency_signs: list[str]
    disclaimer: str
