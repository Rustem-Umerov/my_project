import json
from pathlib import Path

from src.logger_config import get_logger

logs_dir = Path(__file__).resolve().parent.parent / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)  # Создаем директорию, если отсутствует
logs_file = logs_dir / "utils.log"

logger = get_logger(
    __name__,
    level="DEBUG",
    log_file=str(logs_file),
    fmt="%(asctime)s - %(module)s - %(levelname)s - %(message)s",
    mode="w",
)


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
                logger.error("Содержимое файла %s не является списком. Функция возвращает пустой список.", file_path)
                return []

    # Ниже, помимо FileNotFoundError, также есть обработка json.JSONDecodeError – если JSON поврежден,
    # функция вернет пустой список, а не вызовет ошибку.
    except (FileNotFoundError, json.JSONDecodeError):
        logger.exception(
            "Произошла ошибка при открытии или разборе файла %s. Функция возвращает пустой список.", file_path
        )
        return []


base_dir = Path(__file__).resolve().parent  # Определяем базовый путь относительно текущего файла
# Ниже формируем путь к json-файлу, который находится в папке 'data' внутри базовой директории
json_path = base_dir.parent / "data" / "operations.json"

financial_operations_result = financial_operations(json_path)
