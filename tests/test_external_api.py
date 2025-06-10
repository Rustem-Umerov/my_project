from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from pytest import LogCaptureFixture
from requests import RequestException

from src.external_api import convert_to_rub, transaction


@pytest.mark.parametrize(
    "input_dict",
    [
        15151515,
        "abs",
        [11, 12, 13],
        ["abs", "abs"],
        ("abs", 123),
    ],
)
def test_transaction_invalid_type(input_dict: Any) -> None:
    """Тест проверяет, что, если функция получает на вход не словарь, то возникает ошибка TypeError."""

    with pytest.raises(TypeError, match="Ожидается словарь с транзакцией, но получен: "):
        transaction(input_dict)


@pytest.mark.parametrize(
    "input_dict, result",
    [
        ({"operationAmount": {"currency": {"name": "руб.", "code": "RUB"}}}, 0.0),
        ({"operationAmount": {"amount": "abs", "currency": {"name": "руб.", "code": "RUB"}}}, 0.0),
        ({"operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}}}, 31957.58),
    ],
)
def test_transaction_dict_input(input_dict: dict, result: float) -> None:
    """Тест проверяет, как отработает функция, если на вход ей поступают словари:
    - без ключа 'amount'
    - с не правильным значение у ключа amount
    - корректный словарь, со значением 'RUB' по ключу 'code'"""

    with patch("src.external_api.convert_to_rub", return_value=31957.58):
        assert transaction(input_dict) == result


@pytest.mark.parametrize(
    "invalid_dict, log_message",
    [
        (
            {"operationAmount": {"currency": {"name": "руб.", "code": "RUB"}}},
            "Ключ 'amount' отсутствует в транзакции.",
        ),
        (
            {"operationAmount": {"amount": "abs", "currency": {"name": "руб.", "code": "RUB"}}},
            "Ошибка преобразования amount",
        ),
    ],
)
def test_transaction_invalid_dict_input_caplog(
    invalid_dict: dict, log_message: str, caplog: LogCaptureFixture
) -> None:
    """Тест проверяет логирование ошибок."""

    transaction(invalid_dict)
    assert log_message in caplog.text


def test_transaction_dict_not_rub() -> None:
    """Тест проверяет, что функция корректно обрабатывает конвертацию валюты,
    если на вход словарь с транзакцией не в RUB"""

    transaction_dict = {"operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}}}

    # Мокаю `convert_to_rub`, чтобы она возвращала фиксированное значение 1000.0
    with patch("src.external_api.convert_to_rub", return_value=1000.0) as mock_convert:
        result = transaction(transaction_dict)

        assert result == 1000.0

        # Проверяю, что `convert_to_rub` была вызвана с правильными аргументами
        mock_convert.assert_called_once_with("USD", 8221.37)


@pytest.mark.parametrize("input_number, result", [(11.11, 11.11), ("11.11", 11.11), ("   11.11", 11.11)])
@patch("os.getenv", return_value="TEST_API_KEY")
@patch("requests.get", autospec=True)
def test_convert_to_rub_valid_data(
    mock_get: MagicMock, _mock_env: MagicMock, input_number: float | str, result: float
) -> None:
    """Тест успешного запроса к API с корректным ответом."""

    mock_get.return_value.raise_for_status = lambda: None  # Заглушка для метода
    mock_get.return_value.json.return_value = {"result": input_number}  # Имитация ответа API

    output = convert_to_rub("USD", 100)
    assert output == result

    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert",
        headers={"apikey": "TEST_API_KEY"},
        params={"amount": 100, "from": "USD", "to": "RUB"},
    )


@patch("requests.get", autospec=True)
def test_convert_to_rub_not_result(mock_get: MagicMock, caplog: LogCaptureFixture) -> None:
    """Тест проверяет, что если ответ API не содержит ключ 'result',
    функция возвращает 0.0 и логирует соответствующую ошибку."""

    mock_get.return_value.raise_for_status = lambda: None  # Заглушка для метода
    mock_get.return_value.json.return_value = {}  # Имитация ответа API

    output = convert_to_rub("USD", 100)

    assert output == 0.0
    assert "Ключ 'result' отсутствует в ответе API." in caplog.text


@pytest.mark.parametrize("input_str", ["    ", ""])
@patch("requests.get", autospec=True)
def test_convert_to_rub_invalid_str(mock_get: MagicMock, input_str: str, caplog: LogCaptureFixture) -> None:
    """Тест проверяет, что если значение по ключу "result" приходит как строка,
    но после вызова strip() она оказывается пустой, функция должна залогировать ошибку и вернуть 0.0."""

    mock_get.return_value.raise_for_status = lambda: None  # Заглушка для метода
    mock_get.return_value.json.return_value = {"result": input_str}  # Имитация ответа API

    output = convert_to_rub("USD", 100)

    assert output == 0.0
    assert "Результат API содержит только пробельные символы или пустую строку." in caplog.text


@pytest.mark.parametrize("invalid_input", ["abs", "123abs123"])
@patch("requests.get", autospec=True)
def test_convert_to_rub_invalid_conversion(mock_get: MagicMock, invalid_input: str, caplog: LogCaptureFixture) -> None:
    """Тест проверяет, что если значение по ключу "result" не может быть преобразовано в float,
    функция должна залогировать ошибку и вернуть 0.0."""

    mock_get.return_value.raise_for_status = lambda: None  # Заглушка для метода
    mock_get.return_value.json.return_value = {"result": invalid_input}  # Имитация ответа API

    output = convert_to_rub("USD", 100)

    assert output == 0.0
    assert "Ошибка преобразования результата API" in caplog.text


@patch("requests.get", autospec=True)
def test_convert_to_rub_connection_error(mock_get: MagicMock, caplog: LogCaptureFixture) -> None:
    """Тест проверяет, что если при вызове requests.get происходит ошибка (например, RequestException),
    функция обрабатывает исключение, логирует ошибку и возвращает 0.0."""

    mock_get.side_effect = RequestException("API недоступен")

    output = convert_to_rub("USD", 100)

    assert output == 0
    assert "Ошибка при обращении к API конвертации:" in caplog.text
