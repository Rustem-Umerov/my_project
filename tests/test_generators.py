import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions
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


# Ниже декоратор для тестовой функции test_card_number_generator.
@pytest.mark.parametrize(
    "start, stop, result",
    [
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        ),
        (
            9999999999999995,
            9999999999999999,
            [
                "9999 9999 9999 9995",
                "9999 9999 9999 9996",
                "9999 9999 9999 9997",
                "9999 9999 9999 9998",
                "9999 9999 9999 9999",
            ],
        ),
        (10, 10, ["0000 0000 0000 0010"]),
    ],
)
def test_card_number_generator(start: int, stop: int, result: list[str]) -> None:
    """Тест проверяет, что генератор выдает правильные номера карт в заданном диапазоне."""

    assert list(card_number_generator(start, stop)) == result


# Ниже декоратор для тестовой функции test_card_number_generator_error.
@pytest.mark.parametrize(
    "start, stop, error",
    [(5, 1, ValueError), (0, 5, ValueError), (9999999999999995, 9999999999999910, ValueError), (-10, 10, ValueError)],
)
def test_card_number_generator_error(start: int, stop: int, error: type[ValueError]) -> None:
    """Тест проверяет, что будет вызвана ошибка, если на вход поступят не корректные данные."""

    with pytest.raises(error):
        list(card_number_generator(start, stop))


# Ниже декоратор для тестовой функции test_card_number_generator_stop_iteration.
@pytest.mark.parametrize(
    "start, stop, result",
    [
        (1, 1, StopIteration),
        (156, 156, StopIteration),
        (8596, 8596, StopIteration),
    ],
)
def test_card_number_generator_stop_iteration(start: int, stop: int, result: type[StopIteration]) -> None:
    """Тест проверяет, что после исчерпания всех элементов
    дальнейшие вызовы next() выбрасывают исключение StopIteration"""

    generator = card_number_generator(start, stop)
    next(generator)  # Получает первый и единственный элемент генератора.

    with pytest.raises(result):
        next(generator)
