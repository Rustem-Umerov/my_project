from typing import Any, Iterator


def filter_by_currency(transactions: list[dict[str, Any]], currency: str) -> Iterator[dict[str, Any]]:
    """Функция принимает на вход список словарей, представляющих транзакции.
    Функция возвращает итератор, который поочередно выдает транзакции, где валюта операции соответствует заданной"""

    filter_list_dict = filter(
        lambda x: x.get("operationAmount", {}).get("currency", {}).get("name", "").lower() == currency.lower(),
        transactions,
    )

    return filter_list_dict
