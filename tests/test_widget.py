import pytest

from src.widget import mask_account_card


@pytest.mark.parametrize(
    "user_input, result",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Visa Platinum 11111111", "Visa Platinum 11111111"),
        ("Vi@sa Pl@atinum 11111111", "Vi@sa Pl@atinum 11111111"),
        ("Счет 1111111111", "Счет 1111111111"),
        ("С@чет 1111111111", "С@чет 1111111111"),
    ],
)
def test_mask_account_card(user_input: str, result: str) -> None:
    assert mask_account_card(user_input) == result


def test_mask_account_card_error() -> None:
    with pytest.raises(TypeError):
        mask_account_card(7000792289606361)  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        mask_account_card(73654108430135874305)  # type: ignore[arg-type]
