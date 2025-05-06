from typing import Any

import pytest

from src.widget import get_date, mask_account_card, output_result

VALID_CARD = ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361")
VALID_ACCOUNT = ("Счет 73654108430135874305", "Счет **4305")


# Ниже декоратор для тестовой функции test_mask_account_card.
@pytest.mark.parametrize(
    "user_input, result",
    [
        VALID_CARD,
        VALID_ACCOUNT,
        ("Visa Platinum 11111111", "Visa Platinum 11111111"),
        ("Vi@sa Pl@atinum 11111111", "Vi@sa Pl@atinum 11111111"),
        ("Счет 1111111111", "Счет 1111111111"),
        ("С@чет 1111111111", "С@чет 1111111111"),
        ("", ""),
    ],
)
def test_mask_account_card(user_input: str, result: str) -> None:
    """Проверяет, что функция корректно маскирует строку, содержащую тип и номер карты или номер счета.
    Если строка, переданная в функцию, правильная, то функция ее маскирует.
    Если строка, переданная в функцию, содержит хотя бы одну ошибку, то функция возвращает строку без изменения."""

    assert mask_account_card(user_input) == result


# Ниже декоратор для тестовой функции test_mask_account_card_error.
@pytest.mark.parametrize(
    "invalid_input, result", [(7000792289606361, TypeError), (73654108430135874305, TypeError), (None, TypeError)]
)
def test_mask_account_card_error(invalid_input: Any, result: type[TypeError]) -> None:
    """Проверяет, что возникнет ошибка, в том случае, если тип данных, переданных
    в функцию, будет не строковым."""

    with pytest.raises(result):
        mask_account_card(invalid_input)


# Ниже декоратор для тестовой функции test_output_result.
@pytest.mark.parametrize(
    "user_input, result",
    [
        VALID_CARD,
        VALID_ACCOUNT,
    ],
)
def test_output_result(user_input: str, result: str) -> None:
    """Проверяет, что функция корректно маскирует строку, содержащую тип и номер карты или номер счета.
    Данная функция маскирует исключительно корректные данные.
    Если переданные данные содержат не правильные, то возникает ошибка."""

    assert output_result(user_input) == result


# Ниже декоратор для тестовой функции test_output_result_error.
@pytest.mark.parametrize(
    "invalid_input, result",
    [
        ("Visa Platinum 111111", ValueError),
        ("Счет 1111111111", ValueError),
        ("V@isa P@latinu1m 7000792289606361", ValueError),
        ("Сче1т 73654108430135874305", ValueError),
        (7000792289606361, TypeError),
        (73654108430135874305, TypeError),
        (None, TypeError),
    ],
)
def test_output_result_error(invalid_input: Any, result: type[ValueError | TypeError]) -> None:
    """Проверяет, что возникнет ошибка:
    ValueError, если строка, содержащая тип и номер карты или номер счета будет содержать ошибки,
    TypeError, если тип данных, переданных в функцию, будет не строковым."""

    with pytest.raises(result):
        output_result(invalid_input)


# Ниже декоратор для тестовой функции test_get_date.
@pytest.mark.parametrize(
    "str_date, result",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024-03-11T02:26:18.6", "11.03.2024"),
        ("2024-01-01T00:00:00", "01.01.2024"),
    ],
)
def test_get_date(str_date: str, result: str) -> None:
    """Проверяет, что функция возвращает дату в формате "ДД.ММ.ГГГГ"""

    assert get_date(str_date) == result


# Ниже декоратор для тестовой функции test_get_date_error.
@pytest.mark.parametrize(
    "invalid_input, result",
    [
        ("202-03-11T02:26:18.671407", ValueError),
        ("2024-3-11T02:26:18.671407", ValueError),
        ("2024-03-1T02:26:18.671407", ValueError),
        ("", ValueError),
        (None, TypeError),
        (20240311, TypeError),
    ],
)
def test_get_date_error(invalid_input: Any, result: type[ValueError | TypeError]) -> None:
    """Проверяет, что возникает ошибка:
    ValueError, если передать в функцию неправильный формат даты и времени,
    TypeError, если тип данных, переданных в функцию, будет не строковым.
    """

    with pytest.raises(result):
        get_date(invalid_input)
