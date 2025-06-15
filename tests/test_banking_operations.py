import pytest

from src.banking_operations import process_bank_search, process_bank_operations


@pytest.mark.parametrize(
    "search_str, result_list",
    [
        ("Перевод организации", [{"description": "Перевод организации"}, {"description": "Перевод организации"}]),
        ("Открытие вклада", [{"description": "Открытие вклада"}, {"description": "Открытие вклада"}]),
        (
            "перевод с карты на карту",
            [{"description": "Перевод с карты на карту"}, {"description": "Перевод с карты на карту"}],
        ),
        (
            "перевод со счета на счет",
            [{"description": "Перевод со счета на счет"}, {"description": "Перевод со счета на счет"}],
        ),
    ],
)
def test_process_bank_search(transaction_data: list[dict], search_str: str, result_list: list[dict]) -> None:
    """Тест проверяет, что функция правильно фильтрует словари с транзакциями."""

    result = process_bank_search(transaction_data, search_str)
    assert result == result_list


@pytest.mark.parametrize(
    "search_str, result_list",
    [
        ("Перевод организации", []),
        ("Открытие вклада", []),
        ("Перевод с карты на карту", []),
        ("Перевод со счета на счет", []),
    ],
)
def test_process_bank_search_invalid_data(
    transaction_invalid_data: list[dict], search_str: str, result_list: list[dict]
) -> None:
    """Тест проверяет, что функция не вызывает ошибку, если на вход поступают не правильные данные."""

    result = process_bank_search(transaction_invalid_data, search_str)
    assert result == result_list


@pytest.mark.parametrize(
    "not_list, input_str",
    [
        ("abc", "Открытие вклада"),
        (123, "Открытие вклада"),
        (({"description": "Перевод со счета на счет"}, {"description": "Открытие вклада"}), "Открытие вклада"),
    ],
)
def test_process_bank_search_not_list(not_list: list, input_str: str) -> None:
    """Тест проверяет, что если будет не список, а другой тип данных, будет ошибка ValueError."""

    with pytest.raises(ValueError):
        process_bank_search(not_list, input_str)


@pytest.mark.parametrize(
    "input_list, not_str",
    [
        ([{"description": "Перевод со счета на счет"}, {"description": "Открытие вклада"}], ["Открытие вклада"]),
        ([{"description": "Перевод со счета на счет"}, {"description": "Открытие вклада"}], ("Открытие вклада",)),
        ([{"description": "Перевод со счета на счет"}, {"description": "Открытие вклада"}], 123),
    ],
)
def test_process_bank_search_not_str(input_list: list, not_str: str) -> None:
    """Тест проверяет, что если будет не строка, а другой тип данных, будет ошибка ValueError."""

    with pytest.raises(ValueError):
        process_bank_search(input_list, not_str)


@pytest.mark.parametrize(
    "categories_list, result_dict",
    [
        (["Перевод организации"], {"Перевод организации": 2}),
        (["Перевод организации", "Открытие вклада"], {"Перевод организации": 2, "Открытие вклада": 2}),
        (["Перевод с карты на карту"], {"Перевод с карты на карту": 2}),
        (
            ["Перевод с карты на карту", "Перевод со счета на счет"],
            {"Перевод с карты на карту": 2, "Перевод со счета на счет": 2},
        ),
        (["abc", "cba"], {}),
        ([1234, 1234], {}),
    ],
)
def test_process_bank_operations(transaction_data: list[dict], categories_list: list, result_dict: dict) -> None:
    """Тест проверяет, что функция правильно работает, в разных ситуациях."""

    result = process_bank_operations(transaction_data, categories_list)
    assert result == result_dict


#########


@pytest.mark.parametrize(
    "not_list, input_list",
    [
        ("abc", ["Открытие вклада", "Перевод со счета на счет"]),
        (123, ["Открытие вклада", "Перевод со счета на счет"]),
        (
            ({"description": "Перевод со счета на счет"}, {"description": "Открытие вклада"}),
            ["Открытие вклада", "Перевод со счета на счет"],
        ),
    ],
)
def test_process_bank_operations_transaction_data_not_list(not_list: list, input_list: list) -> None:
    """Тест проверяет, что если будет не список, а другой тип данных, будет ошибка ValueError."""

    with pytest.raises(ValueError):
        process_bank_operations(not_list, input_list)


@pytest.mark.parametrize(
    "input_list, not_list",
    [
        ([{"description": "Перевод со счета на счет"}, {"description": "Открытие вклада"}], "Открытие вклада"),
        ([{"description": "Перевод со счета на счет"}, {"description": "Открытие вклада"}], ("Открытие вклада",)),
        ([{"description": "Перевод со счета на счет"}, {"description": "Открытие вклада"}], 123),
    ],
)
def test_process_bank_operations_categories_not_list(input_list: list, not_list: list) -> None:
    """Тест проверяет, что если будет не список, а другой тип данных, будет ошибка ValueError."""

    with pytest.raises(ValueError):
        process_bank_operations(input_list, not_list)
