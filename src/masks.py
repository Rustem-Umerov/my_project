import re

LENGTH_OF_CARD_NUMBER = 16  # Константа указывающая длину номера банковской карты
LENGTH_OF_ACCOUNT_NUMBER = 20  # Константа указывающая длину номера банковского счета


def is_account(text: str) -> bool:
    """Проверяет, начинается ли строка на сч[её]т."""

    return bool(re.match(r"сч[её]т", text, re.IGNORECASE))


def check_user_input(user_input: str) -> bool:
    """Функция проверяет входные данные от пользователя."""

    if is_account(user_input):
        pattern = rf"^([a-zA-Zа-яёА-ЯЁ]+\s?){{1,2}}\d{{{LENGTH_OF_ACCOUNT_NUMBER}}}\b"
    else:
        pattern = rf"^([a-zA-Zа-яёА-ЯЁ]+\s?){{1,2}}\d{{{LENGTH_OF_CARD_NUMBER}}}\b"
    return bool(re.fullmatch(pattern, user_input))


def get_mask_card_number(card_number: str) -> str:
    """Принимает номер карты. Возвращает в замаскированном виде.
    Видны первые 6 цифр и последние 4 цифры, остальные символы отображаются звездочками,
    номер разбит по блокам по 4 цифры, разделенным пробелами."""

    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"


def get_mask_account(account_number: str) -> str:
    """Принимает на вход номер счета и возвращает его замаскированный вид.
    Видны только последние 4 цифры номера, а перед ними — две звездочки"""

    return f"**{account_number[-4:]}"


def error_message() -> str:
    """Функция выводит сообщение об ошибке, если пользователь
    ввел не верные данные."""

    return f"""
            *** Ошибка - Вы ввели неверные данные ***
        Введите данные в таком формате:
        <<"название карты или счета" "номер карты или счета">>
        Номер карты {LENGTH_OF_CARD_NUMBER} цифр, номер счета {LENGTH_OF_ACCOUNT_NUMBER} цифр.
        """
