import os
from typing import Any, Dict, Union

import requests
from dotenv import load_dotenv

from src.logger_config import get_logger

logger = get_logger(__name__)


def transaction(dict_transaction: dict[str, Any]) -> float:
    """
    Функция, принимает на вход транзакцию в виде словаря и возвращает
    сумму транзакции (amount) в рублях, тип данных — float.

    Если валюта транзакции не RUB, то вызывается функция convert_to_rub, которая обращается к внешнему API
    для получения текущего курса валют и конвертации суммы операции в рубли.

    Если какие-либо данные отсутствуют или некорректны, функция возвращает 0.0 и логирует ошибку.
    """

    # Проверка входных данных. Функция на вход должна принимать словарь.
    if not isinstance(dict_transaction, dict):
        raise TypeError("Ожидается словарь с транзакцией, но получен: " + str(type(dict_transaction)))

    # Ниже извлекаю код валюты и присваиваю значение переменой.
    path_to_key_code = dict_transaction.get("operationAmount", {}).get("currency", {}).get("code")
    # Ниже извлекаю значение суммы и присваиваю переменой.
    path_to_key_amount = dict_transaction.get("operationAmount", {}).get("amount")

    # Проверяю наличие суммы, по ключу "amount".
    if path_to_key_amount is None:
        # Ниже если суммы нет, то логирую ошибку и возвращаю 0.0
        logger.error("Ключ 'amount' отсутствует в транзакции.")
        return 0.0

    # Если сумма есть, то безопасно ее перевожу в float.
    try:
        converted_amount = float(path_to_key_amount)
    except (ValueError, TypeError) as e:
        logger.exception("Ошибка преобразования amount '%s': %s", path_to_key_amount, e)
        return 0.0

    # Если валюта транзакции не RUB, то для конвертации, вызывается функция convert_to_rub.
    if path_to_key_code and path_to_key_amount != "RUB":
        return convert_to_rub(path_to_key_code, converted_amount)

    # Если валюта RUB, просто возвращаем значение.
    return converted_amount


def convert_to_rub(path_to_key_code: str, converted_amount: float) -> float:
    """Функция обращается к внешнему API для получения текущего курса валют и конвертации суммы операции в рубли"""

    # Ниже формирую путь к файлу .env, который находится в корневой папке.
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    # Ниже загружаю переменные окружения из файла .env по указанному пути.
    load_dotenv(dotenv_path=env_path)

    url = "https://api.apilayer.com/exchangerates_data/convert"
    payload: Dict[str, Union[str, int, float]] = {
        "amount": converted_amount,  # converted_amount это переменная со значением ключа "amount" в типе float.
        "from": path_to_key_code,
        "to": "RUB",
    }
    headers = {"apikey": os.getenv("API_KEY")}

    try:
        # Ниже отправляю GET-запрос к API с заданными заголовками и параметрами
        response = requests.get(url, headers=headers, params=payload)
        # Ниже проверяю статус ответа. Если статус-код указывает на ошибку, raise_for_status() выбросит исключение.
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        logger.exception("Ошибка при обращении к API конвертации: %s", e)
        return 0.0

    # Преобразую ответ API из JSON в словарь.
    result = response.json()

    # Проверяю есть ли ключ "result" в словаре result.
    if "result" in result:
        value = result.get("result", 0.0)
        # Ниже проверяю значение по ключу "result", если str, убираю пробельные символы. Если строка стала пустой,
        # то получается, строка состояла только из пробельных символов.
        if isinstance(value, str):
            value = value.strip()
            if not value:  # Если строка пустая, то логирую ошибку и возвращаю 0.0
                logger.error("Результат API содержит только пробельные символы или пустую строку.")
                return 0.0

        try:
            # Преобразование полученного значение к типу float.
            return float(value)
        except (ValueError, TypeError) as e:
            logger.exception("Ошибка преобразования результата API '%s': %s", value, e)
            return 0.0

    # Если ключа "result" в словаре result нет, то логирую ошибку и возвращаю 0.0
    else:
        logger.error("Ключ 'result' отсутствует в ответе API.")
        return 0.0
