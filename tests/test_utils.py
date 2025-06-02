import json
from pathlib import Path
from unittest.mock import mock_open, patch

from src.utils import financial_operations


def test_financial_operations_valid() -> None:
    """Тест для случая, когда функция financial_operations() на вход получает корректный json-файл
    с корректным JSON-списком транзакций."""

    # expected_data - это ожидаемые данные в виде списка словарей.
    expected_data = [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560",
        },
    ]

    json_data = json.dumps(expected_data)  # Преобразую список в JSON-строку.

    # Патчу open, чтобы вместо реального файла возвращалось наше json_data
    with patch("builtins.open", mock_open(read_data=json_data)) as mocked_open:
        result = financial_operations(Path("file.json"))

        assert result == expected_data

        # Проверяю, что open вызван с нужными аргументами
        mocked_open.assert_called_once_with(Path("file.json"), encoding="utf-8")


def test_financial_operations_not_list() -> None:
    """Тест для случая, когда функция financial_operations() на вход получает корректный json-файл,
    но содержимое файла не является списком (например, словарь)"""

    not_list_data = {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560",
    }
    json_data = json.dumps(not_list_data)

    with patch("builtins.open", mock_open(read_data=json_data)):
        result = financial_operations(Path("file.json"))

        # Так как данные не являются списком, функция должна вернуть пустой список.
        assert result == []


def test_financial_operations_not_json_file() -> None:
    """Тест для случая, когда файл отсутствует."""

    # Патчу open так, чтобы он сразу выбрасывал FileNotFoundError.
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = financial_operations(Path("file.json"))

        assert result == []


def test_financial_operations_invalid_json_file() -> None:
    """Тест для случая, содержимое json-файла - поврежденный JSON."""

    # Ниже переменная invalid_json со строкой, которая не является корректным JSON.
    invalid_json = '{"key": ,"value",}'

    with patch("builtins.open", mock_open(read_data=invalid_json)):
        result = financial_operations(Path("file.json"))

        # При возникновении JSONDecodeError функция должна вернуть пустой список.
        assert result == []
