import pytest

from src.generators import filter_by_currency
from tests.transactions import RUB_TRANSACTIONS, TRANSACTIONS_WITHOUT_CURRENCY, USD_TRANSACTIONS


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
