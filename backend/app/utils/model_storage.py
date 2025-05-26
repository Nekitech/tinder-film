import os
import pickle
from typing import Any


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
