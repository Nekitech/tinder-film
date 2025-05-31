import os
import pickle
from typing import Any

import numpy as np
from implicit.als import AlternatingLeastSquares
from surprise import AlgoBase
from surprise.dump import dump, load


def save_surprise_model(model: AlgoBase, path: str):
    dump(path, algo=model)


class ModelStorage:
    def __init__(self, path: str):
        self.path = path

    def save(self, model: Any) -> None:
        """
        Сохраняет модель в указанный путь.
        """
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "wb") as f:
            pickle.dump(model, f)
        print(f"✅ Модель сохранена: {self.path}")

    def load(self) -> Any:
        """
        Загружает модель из файла.
        """
        if not os.path.exists(self.path):
            print(f"⚠️ Файл модели не найден: {self.path}")
            return None

        with open(self.path, "rb") as f:
            model = pickle.load(f)
        print(f"✅ Модель загружена: {self.path}")
        return model

    def exists(self) -> bool:
        return os.path.exists(self.path)

    def delete(self) -> None:
        """
        Удаляет файл модели.
        """
        if self.exists():
            os.remove(self.path)
            print(f"🗑️ Модель удалена: {self.path}")

    def load_surprise_model(self, path: str) -> AlgoBase:
        _, model = load(path)
        return model

    def save_implicit_model(self, model: AlternatingLeastSquares, path: str):
        np.savez(path, user_factors=model.user_factors, item_factors=model.item_factors)

    def load_implicit_model(self, path: str) -> AlternatingLeastSquares:
        model = AlternatingLeastSquares(factors=50)
        data = np.load(path)
        model.user_factors = data["user_factors"]
        model.item_factors = data["item_factors"]
        return model
