from typing import List

from pydantic import BaseModel


class SimilarUsersResponse(BaseModel):
    user_id: int
    similar_users: List[int]
