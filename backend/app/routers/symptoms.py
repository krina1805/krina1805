from fastapi import APIRouter

from app.schemas.symptom_schema import SymptomRequest, SymptomResponse
from app.services.symptom_service import build_symptom_education

router = APIRouter(prefix="/symptoms", tags=["symptoms"])


@router.post("", response_model=SymptomResponse)
def symptom_info(payload: SymptomRequest) -> SymptomResponse:
    return build_symptom_education(payload.symptoms)
