from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split

from app.repositories.recommendation_data import RecommenderRepository
from app.utils.model_storage import ModelStorage


class RecommenderService:
    def __init__(self, repository: RecommenderRepository, model_storage: ModelStorage):
        self.repo = repository
        self.model = None
        self.model_storage = model_storage

    async def train_model(self, limit: int = 1000):
        ratings_df = await self.repo.get_ratings_df(limit=limit)
        reader = Reader(rating_scale=(0.5, 5.0))
        data = Dataset.load_from_df(ratings_df[["user_id", "movie_id", "rating"]], reader)
        trainset, _ = train_test_split(data, test_size=0.2)

        self.model = SVD()
        self.model.fit(trainset)
        self.model_storage.save(self.model)

    async def get_top_n(self, user_id: int, n: int = 5, limit: int = 1000):
        if self.model is None:
            raise ValueError("Модель ещё не обучена. Сначала вызовите метод train_model.")

        ratings_df = await self.repo.get_ratings_df(limit=limit)
        all_movie_ids = ratings_df["movie_id"].unique()
        rated_ids = ratings_df[ratings_df["user_id"] == user_id]["movie_id"].values
        unrated_ids = [mid for mid in all_movie_ids if mid not in rated_ids]

        predictions = [self.model.predict(user_id, mid) for mid in unrated_ids]
        predictions.sort(key=lambda x: x.est, reverse=True)
        top_n_predictions = predictions[:n]
        top_n_movie_ids = [pred.iid for pred in top_n_predictions]

        movie_titles = await self.repo.get_movie_titles(top_n_movie_ids)

        return [
            {
                "movie_id": pred.iid,
                "title": movie_titles.get(pred.iid, "Unknown Title"),
                "predicted_rating": pred.est
            }
            for pred in top_n_predictions
        ]

    def load_model(self):
        self.model, _ = self.model_storage.load()
