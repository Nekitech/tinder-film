from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split

from app.db.interactioins import InteractionsRepository
from app.repositories.recommendation_data import RecommenderRepository
from app.services.implicit_service import ImplicitFeedbackService
from app.utils.model_storage import ModelStorage


class RecommenderService:
    def __init__(self,
                 repository: RecommenderRepository,
                 model_storage: ModelStorage,
                 interactions_repo: InteractionsRepository,
                 implicit_service: ImplicitFeedbackService):
        self.repo = repository
        self.model = None  # Surprise SVD модель
        self.model_storage = model_storage
        self.interactions_repo = interactions_repo
        self.implicit_service = implicit_service

    async def train_model(self, limit: int = 1000):
        # Тренируем модель SVD на основе рейтингов
        ratings_df = await self.repo.get_ratings_df(limit=limit)
        reader = Reader(rating_scale=(0.5, 5.0))
        data = Dataset.load_from_df(ratings_df[["user_id", "movie_id", "rating"]], reader)
        trainset, _ = train_test_split(data, test_size=0.2)

        self.model = SVD()
        self.model.fit(trainset)
        self.model_storage.save(self.model)

        # Обучаем также модель Implicit на основе лайков
        await self.implicit_service.train()

    async def get_top_n(self, user_id: id, n: int = 5, limit: int = 1000):
        if self.model is None:
            raise ValueError("Модель ещё не обучена. Сначала вызовите метод train_model.")

        # ----- Prediction через Surprise -----
        ratings_df = await self.repo.get_ratings_df(limit=limit)
        all_movie_ids = ratings_df["movie_id"].unique()

        # Фильтруем уже оцененные фильмы (рейтинг + interactions)
        user_interactions = await self.interactions_repo.get_user_interactions(user_id)
        rated_ids = {interaction.movie_id for interaction in user_interactions}
        rated_ids.update(ratings_df[ratings_df["user_id"] == user_id]["movie_id"].values)

        unrated_ids = [mid for mid in all_movie_ids if mid not in rated_ids]

        svd_predictions = [
            (mid, self.model.predict(user_id, mid).est)
            for mid in unrated_ids
        ]
        svd_predictions.sort(key=lambda x: x[1], reverse=True)

        # ----- Prediction через Implicit -----
        implicit_recommendations = await self.implicit_service.get_top_n(user_id, n)

        # ----- Объединяем рекомендации -----
        # Взвешиваем предсказания. Вес для Surprise (рейтинги) — 0.7, для Implicit (лайки) — 0.3.
        recommendations = []
        for movie_id, svd_score in svd_predictions[:n]:
            implicit_score = 0
            if movie_id in implicit_recommendations:
                implicit_score = 1  # Лайк дает сильный вес

            combined_score = 0.7 * svd_score + 0.3 * implicit_score
            recommendations.append((movie_id, combined_score))

        # Сортируем финальный список рекомендаций
        recommendations.sort(key=lambda x: x[1], reverse=True)
        top_n_movie_ids = [rec[0] for rec in recommendations[:n]]

        # Получаем названия фильмов
        movie_titles = await self.repo.get_movie_titles(top_n_movie_ids)

        return [
            {
                "movie_id": movie_id,
                "title": movie_titles.get(movie_id, "Unknown Title"),
                "score": score,
            }
            for movie_id, score in recommendations[:n]
        ]

    def load_model(self):
        self.model, _ = self.model_storage.load()

    async def create_rating(self, user_id: int, movie_id: int, rating: float):
        """
        Обрабатывает логику создания новой оценки.
        :param user_id: ID пользователя
        :param movie_id: ID фильма
        :param rating: Оценка (от 1.0 до 5.0)
        :return: Информация об оценке
        """
        if rating < 1.0 or rating > 5.0:
            raise ValueError("Rating must be between 1.0 and 5.0")

        return await self.repo.create_rating(user_id, movie_id, rating)
