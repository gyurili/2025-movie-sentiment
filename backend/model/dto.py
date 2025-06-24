from pydantic import BaseModel
from typing import Optional


class MovieCreate(BaseModel):
    title: str
    release_date: Optional[str] = None
    director: str
    category: str
    poster_url: Optional[str] = None

class ReviewCreate(BaseModel):
    author: str
    content: str
    
class ReviewOut(BaseModel):
    id: int
    author: str
    content: str
    sentiment: str
    score: int

    model_config = {
        "from_attributes": True
    }

class SentimentRequest(BaseModel):
    text: str
    model_name: Optional[str] = None