import re


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
