from typing import Any, Iterator


def filter_by_currency(transactions: list[dict[str, Any]], currency: str) -> Iterator[dict[str, Any]]:
    """Функция принимает на вход список словарей, представляющих транзакции.
    Функция возвращает итератор, который поочередно выдает транзакции, где валюта операции соответствует заданной"""

    filter_list_dict = filter(
        lambda x: (x.get("operationAmount", {}).get("currency", {}).get("code") or "").lower() == currency.lower(),
        transactions,
    )

    return filter_list_dict


def transaction_descriptions(transactions: list[dict[str, Any]]) -> Iterator[str]:
    """Генератор, который принимает список словарей с транзакциями
    и возвращает описание каждой операции по очереди."""

    for item in transactions:
        description = item.get("description", "")
        # Ниже условие проверяет, что description существует и не является ложным значением,
        # а затем уже вызывается strip(), чтобы убедиться, что строка, очищенная от пробелов, также не пустая.
        if description and description.strip():
            yield description


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Генератор, который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX, где X — цифра номера карты,
    если указан правильный диапазон. Иначе, будет ошибка.
    Генератор может сгенерировать номера карт в заданном диапазоне от start до stop."""

    if not _validate_range(start, stop):
        error_msg = (
            f"Некорректный диапазон генерации.\n"
            f"Допустимый диапазон: 1 ≤ start ≤ stop ≤ 9999999999999999\n"
            f"Вы ввели: : start={start}, stop={stop}"
        )
        raise ValueError(error_msg)

    for num in range(start, stop + 1):
        yield _format_card_number(num)


def _validate_range(start: int, stop: int) -> bool:
    """Функция проверяет, соответствует ли указанный диапазон заданным критериям."""

    return bool(1 <= start <= stop <= 9999999999999999)


def _format_card_number(num: int) -> str:
    """Функция форматирует число, как номер карты XXXX XXXX XXXX XXXX, где X — цифра номера карты"""

    str_number = f"{num:016d}"
    return f"{str_number[:4]} {str_number[4:8]} {str_number[8:12]} {str_number[12:]}"
