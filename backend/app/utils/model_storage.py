import json
import os
import pickle
from typing import Optional

import numpy as np
from implicit.als import AlternatingLeastSquares
from surprise import AlgoBase
from surprise.dump import dump


def save_surprise_model(model: AlgoBase, path: str):
    dump(path, algo=model)


def convert_np(obj):
    import numpy as np

    if isinstance(obj, dict):
        return {
            convert_np(k): convert_np(v) for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [convert_np(v) for v in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_np(v) for v in obj)
    elif isinstance(obj, set):
        return {convert_np(v) for v in obj}
    elif isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    else:
        return obj


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

    def save_implicit_model(self, model: AlternatingLeastSquares):
        """
        Сохраняет модель ALS в файл, включая user_factors и item_factors.
        """
        np.savez(self.path, user_factors=model.user_factors, item_factors=model.item_factors)

    def load_implicit_model(self) -> AlternatingLeastSquares:
        """
        Загружает модель ALS из файла.
        """
        data = np.load(self.path)
        model = AlternatingLeastSquares(factors=data['user_factors'].shape[1])
        model.user_factors = data['user_factors']
        model.item_factors = data['item_factors']
        return model

    def save_mappings(self, mappings: dict):
        from pathlib import Path
        import json

        file_path = Path("app/models/") / "mappings.json"

        # Преобразуем данные перед сериализацией
        serializable_mappings = convert_np(mappings)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(serializable_mappings, f, indent=4, ensure_ascii=False)

    def load_mappings(self) -> dict:
        """
        Загружает маппинг пользователей и фильмов из JSON-файла.
        Если файл пустой или отсутствует, выбрасывает понятную ошибку.
        """
        from pathlib import Path

        file_path = Path("app/models/") / "mappings.json"

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Mapping file not found: {file_path}")

        # Check if file is empty
        if os.path.getsize(file_path) == 0:
            raise ValueError(f"Mapping file is empty: {file_path}")

        # Attempt to load the JSON content
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                mappings = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON from file '{file_path}': {str(e)}")

        # Process and validate the mappings (optional)
        return {
            key: {int(k): v for k, v in value.items()}
            for key, value in mappings.items()
        }
