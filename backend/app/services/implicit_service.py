import pandas as pd
from implicit.als import AlternatingLeastSquares
from scipy.sparse import coo_matrix

from app.repositories.recommendation_data import RecommenderRepository
from app.utils.model_storage import ModelStorage


class ImplicitFeedbackService:
    def __init__(self, repository: RecommenderRepository, model_storage: ModelStorage):
        self.repository = repository
        self.model_path = "app/models/implicit_model.npz"
        self.model_storage = model_storage
        self.model: AlternatingLeastSquares | None = None
        self.user_mapping = {}
        self.item_mapping = {}
        self.reverse_item_mapping = {}

    async def train(self):
        likes_df: pd.DataFrame = await self.repository.get_likes_df()
        likes_df["score"] = 1  # Можно изменить стратегию весов при необходимости

        user_ids = likes_df["user_id"].unique()
        item_ids = likes_df["item_id"].unique()

        self.user_mapping = {uid: idx for idx, uid in enumerate(user_ids)}
        self.item_mapping = {iid: idx for idx, iid in enumerate(item_ids)}
        self.reverse_item_mapping = {idx: iid for iid, idx in self.item_mapping.items()}

        row = likes_df["user_id"].map(self.user_mapping).values
        col = likes_df["item_id"].map(self.item_mapping).values
        data = likes_df["score"].values

        matrix = coo_matrix((data, (row, col)), shape=(len(user_ids), len(item_ids)))

        model = AlternatingLeastSquares(factors=50, iterations=10)
        model.fit(matrix)

        self.model = model
        self.model_storage.save_implicit_model(model, self.model_path)

    async def get_top_n(self, user_id: int, n: int = 5) -> list[int]:
        if self.model is None:
            self.model = self.model_storage.load_implicit_model(self.model_path)

        if user_id not in self.user_mapping:
            return []

        user_idx = self.user_mapping[user_id]
        recommendations = self.model.recommend(user_idx, self.model.item_factors, N=n)

        item_indices = [item_idx for item_idx, _ in recommendations]
        return [self.reverse_item_mapping[i] for i in item_indices]
