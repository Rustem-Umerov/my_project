from typing import Any

import pytest

from src.masks import (LENGTH_OF_ACCOUNT_NUMBER, LENGTH_OF_CARD_NUMBER, check_user_input, error_message,
                       get_mask_account, get_mask_card_number, is_account)


# Ниже декоратор для тестовой функции test_get_mask_card_number.
@pytest.mark.parametrize(
    "number, result",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("7000792289606361abc", "7000 79** **** 6361abc"),
        ("70007922", "7000 79** **** "),
        ("", " ** **** "),
    ],
)
def test_get_mask_card_number(number: str, result: str) -> None:
    """Проверяет, что функция корректно маскирует номер карты.
    Если номер карты не правильный, функция все ровно применяет маскировку,
    так как валидация выполняется в другом месте программы."""

    assert get_mask_card_number(number) == result


# Ниже декоратор для тестовой функции test_get_mask_card_number_error.
@pytest.mark.parametrize(
    "invalid_input, result",
    [
        (1596837868705199, TypeError),
        (None, TypeError),
    ],
)
def test_get_mask_card_number_error(invalid_input: Any, result: type[TypeError]) -> None:
    """Проверяет, что возникнет ошибка, в том случае, если тип данных, переданных
    в функцию, будет не строковым."""

    with pytest.raises(result):
        get_mask_card_number(invalid_input)


# Ниже декоратор для тестовой функции test_get_mask_account.
@pytest.mark.parametrize(
    "number, result",
    [("73654108430135874305", "**4305"), ("7000792289606361abcd", "**abcd"), ("7365410843", "**0843"), ("", "**")],
)
def test_get_mask_account(number: str, result: str) -> None:
    """Проверяет, что функция корректно маскирует номер счета.
    Если номер счета не правильный, функция все ровно применяет маскировку,
    так как валидация выполняется в другом месте программы."""

    assert get_mask_account(number) == result


# Ниже декоратор для тестовой функции test_get_mask_account_error.
@pytest.mark.parametrize(
    "invalid_input, result",
    [
        (73654108430135874305, TypeError),
        (None, TypeError),
    ],
)
def test_get_mask_account_error(invalid_input: Any, result: type[TypeError]) -> None:
    """Проверяет, что возникнет ошибка, в том случае, если тип данных, переданных
    в функцию, будет не строковым."""

    with pytest.raises(result):
        get_mask_account(invalid_input)


def test_error_message() -> None:
    """Проверяет, что вызов функции error_message выводит верное сообщение."""

    assert (
        error_message()
        == f"""
            *** Ошибка - Вы ввели неверные данные ***
        Введите данные в таком формате:
        <<"название карты или счета" "номер карты или счета">>
        Номер карты {LENGTH_OF_CARD_NUMBER} цифр, номер счета {LENGTH_OF_ACCOUNT_NUMBER} цифр.
        """
    )


# Ниже декоратор для тестовой функции test_check_user_input.
@pytest.mark.parametrize(
    "user_input, result",
    [
        ("Visa Platinum 7000792289606361", True),
        ("Счет 73654108430135874305", True),
        ("7000792289606361 Visa Platinum", False),
        ("73654108430135874305 Счет", False),
        ("V1isa P1latinum 7000792289606361", False),
        ("Visa Platinum 7000792289", False),
        ("С1чет 73654108430135874305", False),
        ("Счет 7365410843", False),
    ],
)
def test_check_user_input(user_input: str, result: bool) -> None:
    """Проверяет корректность валидации пользовательского ввода функцией check_user_input."""

    assert check_user_input(user_input) == result


# Ниже декоратор для тестовой функции test_check_user_input_error.
@pytest.mark.parametrize(
    "invalid_input, result",
    [
        (7000792289606361, TypeError),
        (73654108430135874305, TypeError),
        (None, TypeError),
    ],
)
def test_check_user_input_error(invalid_input: Any, result: type[TypeError]) -> None:
    """Проверяет, что возникнет ошибка, в том случае, если тип данных, переданных
    в функцию, будет не строковым."""

    with pytest.raises(result):
        check_user_input(invalid_input)


# Ниже декоратор для тестовой функции test_is_account.
@pytest.mark.parametrize(
    "string, result",
    [
        ("Счет 73654108430135874305", True),
        ("Счет ", True),
        ("Сче", False),
        ("73654108430135874305 Счет", False),
        ("   Счет 73654108430135874305", False),
        ("Visa Platinum 7000792289606361", False),
        ("Visa Platinum", False),
        ("", False),
    ],
)
def test_is_account(string: str, result: bool) -> None:
    """Проверяет, что функция корректно определяет, начинается ли строка на Сч[её]т."""

    assert is_account(string) == result


# Ниже декоратор для тестовой функции test_is_account_error.
@pytest.mark.parametrize(
    "invalid_input, result",
    [
        (73654108430135874305, TypeError),
        (None, TypeError),
    ],
)
def test_is_account_error(invalid_input: Any, result: type[TypeError]) -> None:
    """Проверяет, что возникнет ошибка, в том случае, если тип данных, переданных
    в функцию, будет не строковым."""

    with pytest.raises(result):
        is_account(invalid_input)
