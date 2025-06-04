import os
import pickle
from typing import Optional

import numpy as np
from implicit.als import AlternatingLeastSquares
from surprise import AlgoBase
from surprise.dump import dump, load


def save_surprise_model(model: AlgoBase, path: str):
    dump(path, algo=model)


class ModelStorage:
    def __init__(self, path: str):
        self.path = path

    def save(self, model, trainset: Optional[object] = None):
        """
        Сохраняет модель и, при наличии, trainset в файл.
        """
        data = {"model": model}
        if trainset is not None:
            data["trainset"] = trainset

        with open(self.path, "wb") as f:
            pickle.dump(data, f)

    def load(self):
        """
        Загружает модель и trainset (если он был сохранён).
        """
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Model file {self.path} not found.")
        with open(self.path, "rb") as f:
            data = pickle.load(f)
        return data["model"], data.get("trainset")

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
