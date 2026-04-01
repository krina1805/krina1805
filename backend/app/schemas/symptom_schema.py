from pydantic import BaseModel, Field


class SymptomRequest(BaseModel):
    symptoms: list[str] = Field(min_length=1, max_length=10)


class SymptomResponse(BaseModel):
    symptoms: list[str]
    general_info: str
    when_to_seek_help: str
    emergency_guidance: str
    disclaimer: str
