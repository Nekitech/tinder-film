from surprise import Dataset, Reader, KNNBasic

from app.repositories.similar_user_repository import SimilarUsersRepository
from app.utils.model_storage import ModelStorage


class SimilarUsersService:
    def __init__(self, repository: SimilarUsersRepository, model_storage: ModelStorage):
        self.repo = repository
        self.model = None
        self.trainset = None
        self.model_storage = model_storage

    async def train_model(self, limit: int = 1000, k: int = 5, sim_metric: str = "cosine"):
        ratings_df = await self.repo.get_ratings_df(limit=limit)
        reader = Reader(rating_scale=(0.5, 5.0))
        data = Dataset.load_from_df(ratings_df[["user_id", "movie_id", "rating"]], reader)
        trainset = data.build_full_trainset()

        sim_options = {
            "name": sim_metric,
            "user_based": True
        }

        model = KNNBasic(k=k, sim_options=sim_options)
        model.fit(trainset)

        self.model = model
        self.trainset = trainset
        self.model_storage.save(model, trainset=trainset)

    async def load_model(self):
        self.model, self.trainset = self.model_storage.load()

    async def get_similar_users(self, user_id: int, n: int = 5):
        """
        Fetch similar users by user_id and append username if the user exists in the table.

        :param user_id: Target user ID.
        :param n: Number of similar users to retrieve.
        :return: List of dictionaries with `user_id` and `username`.
        """
        if self.model is None or self.trainset is None:
            raise ValueError("Модель не обучена или не загружена.")

        try:
            inner_id = self.trainset.to_inner_uid(user_id)
        except ValueError:
            return []

        # Get similar user IDs
        neighbor_inner_ids = self.model.get_neighbors(inner_id, k=n)
        similar_user_ids = [int(self.trainset.to_raw_uid(inner_id)) for inner_id in neighbor_inner_ids]

        # Fetch usernames from repository
        similar_users_with_usernames = await self.repo.get_usernames_by_ids(similar_user_ids)

        return similar_users_with_usernames
