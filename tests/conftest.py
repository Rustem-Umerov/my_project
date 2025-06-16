import pytest

from tests.transactions import USD_RUB_TRANSACTIONS


# Ниже fixture со списком разных словарей.
@pytest.fixture
def dict_list() -> list[dict[str, int | str]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 3, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 4, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 5, "state": "PENDING", "date": "2018-09-12T21:27:25.241689"},
        {"id": 6, "state": "PENDING", "date": "2018-10-14T08:21:33.419441"},
        {"id": 7, "state": "FAILED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 8, "state": "FAILED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 9, "state": "FAILED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 10, "state": "FAILED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 11, "state": "FAILED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 12},
        {"id": 13},
    ]


# Ниже fixture со списком словарей, в которых все ключи "state" == "CANCELED".
@pytest.fixture
def list_dict_with_canceled_states() -> list[dict[str, int | str]]:
    return [
        {"id": 41428829, "state": "CANCELED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "CANCELED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


# Ниже fixture возвращает константу USD_RUB_TRANSACTIONS.
@pytest.fixture
def transactions_list() -> list[dict[str, object]]:
    return USD_RUB_TRANSACTIONS


@pytest.fixture
def transaction_data() -> list[dict[str, str]]:
    return [
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод со счета на счет"},
    ]


@pytest.fixture
def transaction_invalid_data() -> list[dict]:
    return [
        {},
        {},
        {"description": [123, "abc"]},
        {"description": 12345},
    ]
