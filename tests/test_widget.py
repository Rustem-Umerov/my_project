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


def test_mask_account_card_error() -> None:
    """Проверяет, что возникнет ошибка, в том случае, если тип данных, переданных
    в функцию, будет не строковым."""

    with pytest.raises(TypeError):
        mask_account_card(7000792289606361)  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        mask_account_card(73654108430135874305)  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        mask_account_card(None)  # type: ignore[arg-type]


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


def test_output_result_error() -> None:
    """Проверяет, что возникнет ошибка:
    ValueError, если строка, содержащая тип и номер карты или номер счета будет содержать ошибки,
    TypeError, если тип данных, переданных в функцию, будет не строковым."""

    with pytest.raises(ValueError):
        output_result("Visa Platinum 111111")

    with pytest.raises(ValueError):
        output_result("Счет 1111111111")

    with pytest.raises(ValueError):
        output_result("V@isa P@latinu1m 7000792289606361")

    with pytest.raises(ValueError):
        output_result("Сче1т 73654108430135874305")

    with pytest.raises(TypeError):
        output_result(7000792289606361)  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        output_result(73654108430135874305)  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        output_result(None)  # type: ignore[arg-type]


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


def test_get_date_error() -> None:
    """Проверяет, что возникает ошибка:
    ValueError, если передать в функцию неправильный формат даты и времени,
    TypeError, если тип данных, переданных в функцию, будет не строковым.
    """

    with pytest.raises(ValueError):
        get_date("202-03-11T02:26:18.671407")

    with pytest.raises(ValueError):
        get_date("2024-3-11T02:26:18.671407")

    with pytest.raises(ValueError):
        get_date("2024-03-1T02:26:18.671407")

    with pytest.raises(ValueError):
        get_date("")

    with pytest.raises(TypeError):
        get_date(None)  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        get_date(20240311)  # type: ignore[arg-type]
