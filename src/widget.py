import re
from datetime import datetime

from src.masks import (LENGTH_OF_ACCOUNT_NUMBER, LENGTH_OF_CARD_NUMBER, check_user_input, error_message,
                       get_mask_account, get_mask_card_number, is_account)


def mask_account_card(type_and_number: str) -> str:
    """Функция принимает один аргумент — строку, содержащую тип и номер карты или номер счета.
    Возвращает строку с замаскированным номером."""

    if is_account(type_and_number):
        return re.sub(rf"\d{{{LENGTH_OF_ACCOUNT_NUMBER}}}", lambda m: get_mask_account(m.group(0)), type_and_number)
    return re.sub(rf"\d{{{LENGTH_OF_CARD_NUMBER}}}", lambda m: get_mask_card_number(m.group(0)), type_and_number)


def output_result(user_input: str) -> str:
    """Функция выводит итоговый результат.
    Сначала данные проверяются, потом возвращает замаскированные данные
    или ошибку при неверном формате"""

    correct_card = check_user_input(user_input)

    if not correct_card:
        raise ValueError(error_message())

    return mask_account_card(user_input)


def get_date(str_data: str) -> str:
    """Функция принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024")."""

    dt = datetime.fromisoformat(str_data)
    return dt.strftime("%d.%m.%Y")
