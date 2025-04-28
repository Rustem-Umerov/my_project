import re
from datetime import datetime

from src.masks import check_user_input, get_mask_account, get_mask_card_number

LENGTH_OF_CARD_NUMBER = 16  # Константа указывающая длину номера банковской карты
LENGTH_OF_ACCOUNT_NUMBER = 20  # Константа указывающая длину номера банковского счета


def mask_account_card(type_and_number: str) -> str:
    """Функция принимает один аргумент — строку, содержащую тип и номер карты или номер счета.
    Возвращает строку с замаскированным номером."""

    if re.match(r"сч[её]т", type_and_number, re.IGNORECASE):
        return re.sub(r"\d{20}", lambda m: get_mask_account(m.group(0)), type_and_number)
    return re.sub(r"\d{16}", lambda m: get_mask_card_number(m.group(0)), type_and_number)


def output_result(user_input: str) -> str:
    """Функция выводит итоговый результат.
    Сначала данные проверяются. Потом происходит маскировка данных."""

    if re.match(r"сч[её]т", user_input, re.IGNORECASE):
        correct_card = check_user_input(user_input, LENGTH_OF_ACCOUNT_NUMBER)
        result_1 = mask_account_card(correct_card)
        return result_1

    correct_card = check_user_input(user_input, LENGTH_OF_CARD_NUMBER)
    result_2 = mask_account_card(correct_card)
    return result_2


def get_date(str_data: str) -> str:
    """Функция принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024")."""

    dt = datetime.fromisoformat(str_data)
    return dt.strftime("%d.%m.%Y")
