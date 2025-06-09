from typing import List, Optional

from pydantic import BaseModel


class SimilarUser(BaseModel):
    user_id: int
    username: Optional[str]  # Username can be null if the user does not exist in the database.


class SimilarUsersResponse(BaseModel):
    user_id: int
    similar_users: List[SimilarUser]  # List of dictionaries with `user_id` and `username`.
