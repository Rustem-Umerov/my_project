from typing import Any, Iterator


def filter_by_currency(transactions: list[dict[str, Any]], currency: str) -> Iterator[dict[str, Any]]:
    """Функция принимает на вход список словарей, представляющих транзакции.
    Функция возвращает итератор, который поочередно выдает транзакции, где валюта операции соответствует заданной"""

    filter_list_dict = filter(
        lambda x: x.get("operationAmount", {}).get("currency", {}).get("name", "").lower() == currency.lower(),
        transactions,
    )

    return filter_list_dict


def transaction_descriptions(transactions: list[dict[str, Any]]) -> Iterator[str]:
    """Генератор, который принимает список словарей с транзакциями
    и возвращает описание каждой операции по очереди."""

    for item in transactions:
        yield item.get("description", "")


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Генератор, который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX, где X — цифра номера карты.
    Генератор может сгенерировать номера карт в заданном диапазоне от start до stop."""

    for num in range(start, stop + 1):
        str_number = f"{num:016d}"
        yield f"{str_number[:4]} {str_number[4:8]} {str_number[8:12]} {str_number[12:]}"
