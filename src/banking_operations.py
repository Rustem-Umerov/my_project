import re
from collections import Counter


def process_bank_search(banking_transaction_data: list[dict], search: str) -> list[dict]:
    """ "Функция, принимает на вход, список словарей с данными о банковских операциях и строку для поиска.
    Возвращает список словарей, с данными о банковских операциях, у которых в описании есть данная строка."""

    pattern = re.compile(search, re.IGNORECASE)
    result_list = []

    for dict_transaction in banking_transaction_data:
        description = dict_transaction.get("description")

        if isinstance(description, str) and pattern.search(description):
            result_list.append(dict_transaction)

    return result_list


def process_bank_operations(banking_transaction_data: list[dict], categories: list) -> dict:
    """Функция, принимает список словарей с данными о банковских операциях и список категорий операций,
    а возвращает словарь, в котором ключи — это названия категорий,
    а значения — это количество операций в каждой категории."""

    categories_set = {category.lower() for category in categories}
    categories_list = []

    for dict_transaction in banking_transaction_data:
        description = dict_transaction.get("description")

        if isinstance(description, str):
            description_lower = description.lower()
            if description_lower in categories_set:
                categories_list.append(description)

    return dict(Counter(categories_list))
