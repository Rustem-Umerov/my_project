from typing import Any

import pytest

from src.processing import filter_by_state


def test_one_filter_by_state(list_dict_with_canceled_states: list[dict[str, int | str]]) -> None:
    """Проверяет работу функции при отсутствии словарей с указанным, по умолчанию, статусом state в списке"""

    assert filter_by_state(list_dict_with_canceled_states) == []


# Ниже декоратор для тестовой функции test_two_filter_by_state.
@pytest.mark.parametrize(
    "state, correct_list_dict",
    [
        ("EXECUTED", [1, 2]),
        ("CANCELED", [3, 4]),
        ("PENDING", [5, 6]),
        ("FAILED", [7, 8, 9, 10, 11]),
        ("NO STATUS", []),
        ("", []),
        (None, [12, 13]),
    ],
)
def test_two_filter_by_state(dict_list: list[dict[str, int | str]], state: Any, correct_list_dict: list[int]) -> None:
    """Проверяет, работу функции, с помощью @pytest.fixture dict_list()"""

    result = filter_by_state(dict_list, state)
    assert [element["id"] for element in result] == correct_list_dict
