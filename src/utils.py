import json
from pathlib import Path

from src.logger_config import get_logger


logger = get_logger(
    __name__,
    level="DEBUG",
    log_file="utils.log",
    fmt="%(asctime)s - %(module)s - %(levelname)s - %(message)s",
    mode="w",
)

base_dir = Path(__file__).resolve().parent  # Определяем базовый путь относительно текущего файла
# Ниже формируем путь к json-файлу, который находится в папке 'data' внутри базовой директории
json_path = base_dir.parent / "data" / "operations.json"


def financial_operations(file_path: Path) -> list[dict]:
    """
    Функция принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """

    try:
        logger.debug("Происходит открытие файла: %s", file_path)
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, list):
                logger.debug("Данные успешно загружены из файла: %s", file_path)
                return data
            else:
                logger.error(
                "Содержимое файла %s не является списком. Функция возвращает пустой список.", file_path)
                return []

    # Ниже, помимо FileNotFoundError, также есть обработка json.JSONDecodeError – если JSON поврежден,
    # функция вернет пустой список, а не вызовет ошибку.
    except (FileNotFoundError, json.JSONDecodeError):
        logger.exception(
        "Произошла ошибка при открытии или разборе файла %s. Функция возвращает пустой список.", file_path
        )
        return []
