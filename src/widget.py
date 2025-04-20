from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(type_and_number: str) -> str:
    """Функция принимает один аргумент — строку, содержащую тип и номер карты или счета.
    Возвращает строку с замаскированным номером."""

    # Делит входную строку на список
    str_split = type_and_number.split()

    # Далее проверка элементов списка. Если первый элемент равен "счет",
    # то последний элемент списка передается в функцию для номера счета,
    # иначе в функцию для номера карты.
    if str_split[0].lower() == "счет" or str_split[0].lower() == "счёт":
        masked_number = get_mask_account(str_split[-1])
        result = [str_split[0], masked_number]

        return " ".join(result)

    masked_card = get_mask_card_number(str_split[-1])
    del str_split[-1]
    result = str_split + [masked_card]

    return " ".join(result)


def get_date(str_data: str) -> str:
    """Функция принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024")."""

    return f"{str_data[8:10]}.{str_data[5:7]}.{str_data[:4]}"
