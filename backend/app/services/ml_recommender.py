import pandas as pd
from sqlalchemy import Table, Column, Integer, Float, MetaData, select, String
from sqlalchemy.ext.asyncio import AsyncSession
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split

from app.utils.model_storage import ModelStorage

metadata = MetaData()

# Декларация таблицы через SQLAlchemy Table
ratings_table = Table(
    "ratings",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("movie_id", Integer, nullable=False),
    Column("rating", Float, nullable=False)
)

movies_table = Table(
    "movies",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False)
)


class RecommenderService:
    def __init__(self, db: AsyncSession, model_storage: ModelStorage):
        self.db = db
        self.model = None
        self.model_storage = model_storage

    async def load_data_from_db(self, limit: int = 1000):
        """
        Загружает данные из базы данных и возвращает DataFrame.

        :param limit: Максимальное количество строк для выборки из базы данных.
        """
        result = await self.db.execute(
            select(
                ratings_table.c.user_id,
                ratings_table.c.movie_id,
                ratings_table.c.rating
            ).limit(limit)
        )
        rows = result.fetchall()

        # Преобразуем данные в Pandas DataFrame
        df = pd.DataFrame(rows, columns=["user_id", "movie_id", "rating"])
        return df

    async def train_model(self, limit: int = 1000):
        """
        Обучает модель на данных, загруженных из базы данных.

        :param limit: Максимальное количество строк для выборки из базы данных.
        """
        # Загрузка данных
        ratings_df = await self.load_data_from_db(limit=limit)

        # Преобразование данных для библиотеки Surprise
        reader = Reader(rating_scale=(0.5, 5.0))
        data = Dataset.load_from_df(ratings_df[["user_id", "movie_id", "rating"]], reader)
        trainset, testset = train_test_split(data, test_size=0.2)

        # Обучение модели SVD
        model = SVD()
        model.fit(trainset)

        self.model = model
        self.model_storage.save(model)

    async def get_top_n(self, user_id: int, n: int = 5, limit: int = 1000):
        """
        Возвращает топ-N рекомендаций для указанного пользователя, включая названия фильмов.

        :param user_id: ID пользователя.
        :param n: Количество рекомендаций.
        :param limit: Количество строк, используемых для поиска подходящих фильмов.
        :return: Список рекомендаций с полями id, title и predicted_rating.
        """

        if self.model is None:
            raise ValueError("Модель ещё не обучена. Сначала вызовите метод train_model.")

        # Загрузить данные из базы данных
        ratings_df = await self.load_data_from_db(limit=limit)

        # Получить список фильмов, которые пользователь ещё не оценил
        all_movie_ids = ratings_df["movie_id"].unique()
        rated = ratings_df[ratings_df["user_id"] == user_id]["movie_id"].values
        unrated = [movie_id for movie_id in all_movie_ids if movie_id not in rated]

        # Предсказать оценки для всех неоцененных фильмов
        predictions = [self.model.predict(user_id, movie_id) for movie_id in unrated]
        predictions.sort(key=lambda x: x.est, reverse=True)

        # Выбрать top-N фильмов
        top_n_predictions = predictions[:n]
        top_n_movie_ids = [pred.iid for pred in top_n_predictions]

        # Запросить названия фильмов из базы данных
        result = await self.db.execute(
            select(
                movies_table.c.id,
                movies_table.c.title
            ).where(movies_table.c.id.in_(top_n_movie_ids))
        )
        rows = result.mappings().all()
        print("movie data:   ", rows)
        movie_data = {row["id"]: row["title"] for row in rows}
        # Объединить данные о предсказаниях с названиями фильмов
        recommendations = []
        for pred in top_n_predictions:
            movie_id = pred.iid
            recommendations.append({
                "movie_id": movie_id,  # Используется поле id
                "title": movie_data.get(movie_id, "Unknown Title"),  # Название фильма
                "predicted_rating": pred.est  # Предсказанный рейтинг
            })

        return recommendations

    def load_model(self):
        self.model = self.model_storage.load()
