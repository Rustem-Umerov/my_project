from typing import Any

import pytest

from src.processing import filter_by_state, sort_by_date


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


# Ниже декоратор для тестовой функции test_sort_by_date.
@pytest.mark.parametrize(
    "reverse, sort_id",
    [
        (True, [1, 6, 7, 8, 10, 3, 4, 5, 2, 9, 11]),
        (False, [2, 9, 11, 3, 4, 5, 6, 7, 8, 10, 1]),
    ],
)
def test_sort_by_date(dict_list: list[dict[str, int | str]], reverse: bool, sort_id: list[int]) -> None:
    """Проверяет корректную сортировку списка словарей по датам в порядке убывания и возрастания."""

    result = sort_by_date(dict_list, reverse)

    assert [i["id"] for i in result] == sort_id


# Ниже декоратор для тестовой функции test_sort_by_date_error.
@pytest.mark.parametrize(
    "list_dict, result",
    [
        (
            [
                {"id": 3, "state": "CANCELED", "date": "2018.09.12"},
                {"id": 4, "state": "CANCELED", "date": "2015.10.16T21:15:25.241689"},
            ],
            ValueError,
        )
    ],
)
def test_sort_by_date_error(list_dict: list[dict[str, str]], result: type[ValueError]) -> None:
    """Проверяет возникновения ошибки, если в функцию передать дату в некорректном или в нестандартном формате."""

    with pytest.raises(result):
        sort_by_date(list_dict)


def test_sort_by_same_date(dict_list: list[dict[str, int | str]]) -> None:
    """Из dict_list формирую список словарей с одинаковой датой: "2018-09-12T21:27:25.241689".
    Далее сортирую данный список и проверяю, что после сортировки словари остаются в том же порядке,
    как были в исходном списке"""

    list_dict_same_date = [d for d in dict_list if d.get("date") == "2018-09-12T21:27:25.241689"]

    result = sort_by_date(list_dict_same_date)

    assert [d["id"] for d in result] == [3, 4, 5]
