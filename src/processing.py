from datetime import datetime

def filter_by_state(list_dict: list, state: str = 'EXECUTED') -> list:
    """Функция принимает список словарей и возвращает новый список словарей,
    содержащий только те словари, у которых ключ state соответствует указанному значению."""

    return [d for d in list_dict if d.get("state") == state]


def sort_by_date(list_dict: list, reverse: bool = True) -> list:
    """Функция принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание)
    и возвращает новый список, отсортированный по дате"""

    return sorted([d for d in list_dict if "date" in d],
                  key=lambda x: datetime.fromisoformat(x["date"]), reverse=reverse)
