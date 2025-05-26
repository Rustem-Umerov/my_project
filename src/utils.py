import json
from pathlib import Path


def financial_operations(file_path: Path) -> list[dict]:
    """
    Функция принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """

    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

            return data if isinstance(data, list) else []

    # Ниже, помимо FileNotFoundError, также есть обработка json.JSONDecodeError – если JSON поврежден,
    # функция вернет пустой список, а не вызовет ошибку.
    except (FileNotFoundError, json.JSONDecodeError):
        return []


base_dir = Path(__file__).resolve().parent  # Определяем базовый путь относительно текущего файла
# Ниже формируем путь к json-файлу, который находится в папке 'data' внутри базовой директории
json_path = base_dir.parent / "data" / "operations.json"

financial_operations_result = financial_operations(json_path)
