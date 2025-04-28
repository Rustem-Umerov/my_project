import re


def check_user_input(user_input: str, length_number: int) -> str:
    """Функция проверяет входные данные от пользователя. Если ввод
    пользователя не соответствует критериям, пользователь должен
    повторить ввод данных."""

    while True:
        pattern = rf"^([a-zA-Zа-яёА-ЯЁ]+\s?){{1,2}}\d{{{length_number}}}\b"

        if re.search(pattern, user_input):
            return user_input

        print(error_message(length_number))
        user_input = input("Повторите попытку: ").strip()


def get_mask_card_number(card_number: str) -> str:
    """Принимает номер карты. Возвращает в замаскированном виде.
    Видны первые 6 цифр и последние 4 цифры, остальные символы отображаются звездочками,
    номер разбит по блокам по 4 цифры, разделенным пробелами."""

    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"


def get_mask_account(account_number: str) -> str:
    """Принимает на вход номер счета и возвращает его замаскированный вид.
    Видны только последние 4 цифры номера, а перед ними — две звездочки"""

    return f"**{account_number[-4:]}"


def error_message(length_number: int) -> str:
    """Функция выводит сообщение об ошибке, если пользователь
    ввел не верные данные."""

    return f"""
            *** Ошибка - Вы ввели неверные данные ***
        Введите данные в таком формате:
        <<"название карты или счета" "номер карты или счета">>
        Номер должен состоять ровно из {length_number} цифр.
        """
