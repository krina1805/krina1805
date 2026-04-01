from pydantic import BaseModel


class Topic(BaseModel):
    name: str
    info: str
    disclaimer: str
