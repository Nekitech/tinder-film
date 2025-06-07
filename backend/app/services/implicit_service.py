import numpy as np
import pandas as pd
from implicit.als import AlternatingLeastSquares
from scipy.sparse import coo_matrix, csr_matrix

from app.db.interactioins import InteractionsRepository
from app.utils.model_storage import ModelStorage


class ImplicitFeedbackService:
    def __init__(self, interactions_repo: InteractionsRepository, model_storage: ModelStorage):
        self.interactions_repo = interactions_repo
        self.model_storage = model_storage
        self.model: AlternatingLeastSquares | None = None
        self.user_mapping = {}
        self.item_mapping = {}
        self.reverse_item_mapping = {}
        self.reverse_user_mapping = {}

    async def train(self):
        interactions = await self.interactions_repo.get_all_interactions()
        if not interactions:
            raise ValueError("Нет взаимодействий для тренировки модели.")

        interactions_df = pd.DataFrame([{
            "user_id": interaction.user_id,
            "movie_id": interaction.movie_id,
            "liked": interaction.liked,
        } for interaction in interactions])

        interactions_df["score"] = interactions_df["liked"].apply(lambda liked: 1 if liked else -1)

        user_ids = interactions_df["user_id"].unique()
        item_ids = interactions_df["movie_id"].unique()

        self.user_mapping = {uid: idx for idx, uid in enumerate(user_ids)}
        self.item_mapping = {iid: idx for idx, iid in enumerate(item_ids)}
        self.reverse_user_mapping = {idx: uid for uid, idx in self.user_mapping.items()}
        self.reverse_item_mapping = {idx: iid for iid, idx in self.item_mapping.items()}

        row = interactions_df["user_id"].map(self.user_mapping).values
        col = interactions_df["movie_id"].map(self.item_mapping).values
        data = interactions_df["score"].values

        matrix = coo_matrix((data, (row, col)), shape=(len(user_ids), len(item_ids)))

        model = AlternatingLeastSquares(factors=50, iterations=10)
        model.fit(matrix)

        self.model_storage.save_implicit_model(model)

        mappings = {
            "user_mapping": self.user_mapping,
            "item_mapping": self.item_mapping,
            "reverse_user_mapping": self.reverse_user_mapping,
            "reverse_item_mapping": self.reverse_item_mapping,
        }
        self.model_storage.save_mappings(mappings)

    async def get_top_n(self, user_id: int, n: int = 5) -> list[int]:
        if self.model is None:
            self._load_model()

        if user_id not in self.user_mapping:
            return []

        user_idx = self.user_mapping[user_id]

        num_items = len(self.item_mapping)
        col = np.arange(num_items)
        data = np.zeros(num_items)
        user_items = csr_matrix((data, (np.zeros(num_items), col)), shape=(1, num_items))

        # Get recommendations using the ALS model
        recommendations = self.model.recommend(user_idx, user_items, N=n)

        # Verify and filter item indices to prevent issues
        valid_item_indices = []
        for item_idx, *_ in recommendations:
            if item_idx in self.reverse_item_mapping:  # Check validity of index
                valid_item_indices.append(self.reverse_item_mapping[item_idx])
            else:
                # Log the problematic index
                print(f"Invalid item index encountered: {item_idx}")

        # Return the filtered valid item indices
        return valid_item_indices

    def _load_model(self):
        self.model = self.model_storage.load_implicit_model()

        mappings = self.model_storage.load_mappings()
        self.user_mapping = mappings["user_mapping"]
        self.item_mapping = mappings["item_mapping"]
        self.reverse_user_mapping = mappings["reverse_user_mapping"]
        self.reverse_item_mapping = mappings["reverse_item_mapping"]
