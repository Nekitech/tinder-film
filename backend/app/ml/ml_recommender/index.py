import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split

# === 1. Загрузка и предобработка данных ===

# Путь к файлам
ratings_path = "dataset/ratings.csv"
movies_path = "dataset/movies.csv"

# Загружаем датасеты
ratings_df = pd.read_csv(ratings_path)
movies_df = pd.read_csv(movies_path)

# Берем только первые 500 фильмов по movieId
top_movies = movies_df.head(500)["movieId"]
filtered_ratings = ratings_df[ratings_df["movieId"].isin(top_movies)]

# === 2. Преобразование в формат surprise ===
reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(filtered_ratings[["userId", "movieId", "rating"]], reader)
trainset, testset = train_test_split(data, test_size=0.2)

# === 3. Обучение модели ===
algo = SVD()
algo.fit(trainset)


# === 4. Рекомендации для одного пользователя ===
def get_top_n(user_id, n=5):
    # Получаем список всех movieId в нашем сабсете
    all_movie_ids = filtered_ratings["movieId"].unique()

    # Ищем фильмы, которые пользователь еще не оценил
    rated = filtered_ratings[filtered_ratings["userId"] == user_id]["movieId"].values
    unrated = [mid for mid in all_movie_ids if mid not in rated]

    # Предсказываем рейтинг
    predictions = [algo.predict(user_id, mid) for mid in unrated]
    predictions.sort(key=lambda x: x.est, reverse=True)

    top_n = predictions[:n]

    # Подставляем названия фильмов
    top_movie_ids = [pred.iid for pred in top_n]
    recommended_titles = movies_df[movies_df["movieId"].isin(top_movie_ids)]

    return recommended_titles[["movieId", "title"]]


# === Пример ===
user_id = 1
top_recommendations = get_top_n(user_id)
print(f"\n🎬 Топ-5 рекомендаций для пользователя {user_id}:")
print(top_recommendations)
