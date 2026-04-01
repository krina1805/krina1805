from pydantic import BaseModel


class TopicResponse(BaseModel):
    topics: list[dict[str, str]]
    disclaimer: str
