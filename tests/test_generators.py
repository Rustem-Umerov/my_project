import pytest

from src.generators import filter_by_currency, transaction_descriptions
from tests.transactions import (RUB_TRANSACTIONS, TRANSACTIONS_WITHOUT_CURRENCY, TRANSACTIONS_WITHOUT_DESCRIPTION,
                                USD_TRANSACTIONS)


# Ниже декоратор для тестовой функции test_filter_by_currency.
@pytest.mark.parametrize(
    "currency, result",
    [
        ("USD", USD_TRANSACTIONS),
        ("RUB", RUB_TRANSACTIONS),
    ],
)
def test_filter_by_currency(
    transactions_list: list[dict[str, int | str]], currency: str, result: list[dict[str, int | str]]
) -> None:
    """Тест использует fixture transactions_list().
    Тест проверяет, что функция корректно фильтрует транзакции по заданной валюте."""

    assert list(filter_by_currency(transactions_list, currency)) == result


# Ниже декоратор для тестовой функции test_filter_by_currency_not_error.
@pytest.mark.parametrize(
    "transactions, currency, result",
    [
        (RUB_TRANSACTIONS, "USD", []),
        (USD_TRANSACTIONS, "RUS", []),
        ([], "RUS", []),
        ([], "USD", []),
        (TRANSACTIONS_WITHOUT_CURRENCY, "USD", []),
    ],
)
def test_filter_by_currency_not_error(transactions: list[dict[str, int | str]], currency: str, result: list) -> None:
    """Тест проверяет, что генератор не завершается ошибкой при обработке пустого списка
    или списка без соответствующих валютных операций."""

    assert list(filter_by_currency(transactions, currency)) == result


# Ниже декоратор для тестовой функции test_transaction_descriptions.
@pytest.mark.parametrize(
    "result_list",
    [
        [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации",
        ]
    ],
)
def test_transaction_descriptions(transactions_list: list[dict[str, int | str]], result_list: list[str]) -> None:
    """Тест использует fixture transactions_list().
    Тест проверяет, что функция возвращает корректные описания для каждой транзакции."""

    assert list(transaction_descriptions(transactions_list)) == result_list


# Ниже декоратор для тестовой функции test_transaction_descriptions_not_error.
@pytest.mark.parametrize(
    "list_dict, result",
    [
        (TRANSACTIONS_WITHOUT_DESCRIPTION, []),
        ([], []),
    ],
)
def test_transaction_descriptions_not_error(list_dict: list, result: list) -> None:
    """Тест проверяет, что функция возвращает пустой список, если на вход поступает
    список словарей с транзакциями без описания или пустой список."""

    assert list(transaction_descriptions(list_dict)) == result
