from fastapi import APIRouter

from app.schemas.topic_schema import TopicResponse
from app.services.topic_service import DISCLAIMER, list_topics

router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("", response_model=TopicResponse)
def get_topics() -> TopicResponse:
    topics = [topic.model_dump() for topic in list_topics()]
    return TopicResponse(topics=topics, disclaimer=DISCLAIMER)
