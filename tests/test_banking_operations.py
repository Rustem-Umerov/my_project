import pytest

from src.banking_operations import process_bank_search


@pytest.mark.parametrize(
    "search_str, result_list",
    [
        ("Перевод организации", [{"description": "Перевод организации"}, {"description": "Перевод организации"}]),
        ("Открытие вклада", [{"description": "Открытие вклада"}, {"description": "Открытие вклада"}]),
        (
            "перевод с карты на карту",
            [{"description": "Перевод с карты на карту"}, {"description": "Перевод с карты на карту"}],
        ),
        (
            "перевод со счета на счет",
            [{"description": "Перевод со счета на счет"}, {"description": "Перевод со счета на счет"}],
        ),
    ],
)
def test_process_bank_search(transaction_data: list[dict], search_str: str, result_list: list[dict]) -> None:
    """Тест проверяет, что функция правильно фильтрует словари с транзакциями."""

    result = process_bank_search(transaction_data, search_str)
    assert result == result_list


@pytest.mark.parametrize(
    "search_str, result_list",
    [
        ("Перевод организации", []),
        ("Открытие вклада", []),
        ("Перевод с карты на карту", []),
        ("Перевод со счета на счет", []),
    ],
)
def test_process_bank_search_invalid_data(
    transaction_invalid_data: list[dict], search_str: str, result_list: list[dict]
) -> None:
    """Тест проверяет, что функция не вызывает ошибку, если на вход поступают не правильные данные."""

    result = process_bank_search(transaction_invalid_data, search_str)
    assert result == result_list
