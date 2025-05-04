import pytest

from src.masks import (
    LENGTH_OF_ACCOUNT_NUMBER,
    LENGTH_OF_CARD_NUMBER,
    check_user_input,
    error_message,
    get_mask_account,
    get_mask_card_number,
    is_account,
)


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


def test_get_mask_card_number_error() -> None:
    """Проверяет, что возникнет ошибка, в том случае, если тип данных, переданных
    в функцию, будет не строковым."""

    with pytest.raises(TypeError):
        get_mask_card_number(1596837868705199)  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        get_mask_card_number(None)  # type: ignore[arg-type]


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


def test_get_mask_account_error() -> None:
    """Проверяет, что возникнет ошибка, в том случае, если тип данных, переданных
    в функцию, будет не строковым."""

    with pytest.raises(TypeError):
        get_mask_account(73654108430135874305)  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        get_mask_account(None)  # type: ignore[arg-type]


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


def test_check_user_input_error() -> None:
    """Проверяет, что возникнет ошибка, в том случае, если тип данных, переданных
    в функцию, будет не строковым."""

    with pytest.raises(TypeError):
        check_user_input(7000792289606361)  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        check_user_input(73654108430135874305)  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        check_user_input(None)  # type: ignore[arg-type]


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


def test_is_account_error() -> None:
    """Проверяет, что возникнет ошибка, в том случае, если тип данных, переданных
    в функцию, будет не строковым."""

    with pytest.raises(TypeError):
        is_account(73654108430135874305)  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        is_account(None)  # type: ignore[arg-type]
