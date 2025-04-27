def filter_by_state(list_dict: list, state: str = 'EXECUTED') -> list:
    """Функция принимает список словарей и возвращает новый список словарей,
    содержащий только те словари, у которых ключ state соответствует указанному значению."""

    return [d for d in list_dict if d.get("state") == state]
