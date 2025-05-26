from typing import List

from pydantic import BaseModel


class Recommendation(BaseModel):
    movie_id: int  # Предсказания используют поле `movie_id`
    title: str
    predicted_rating: float


class RecommendationResponse(BaseModel):
    user_id: int  # Форматированное поле `user_id`
    recommendations: List[Recommendation]
