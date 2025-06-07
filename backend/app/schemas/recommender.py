from typing import List, Optional

from pydantic import BaseModel


class Recommendation(BaseModel):
    movie_id: int  # Предсказания используют поле `movie_id`
    title: str
    score: float
    predicted_rating: Optional[float] = None


class RecommendationResponse(BaseModel):
    user_id: int  # Форматированное поле `user_id`
    recommendations: List[Recommendation]
