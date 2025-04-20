from src.masks import (LENGTH_OF_ACCOUNT_NUMBER, LENGTH_OF_CARD_NUMBER, check_user_input, get_mask_account,
                       get_mask_card_number)


def main() -> None:
    """Данная функция выполняет:
    1) Принимает от пользователя данные (номер банковской карты и номер банковского счета).
    2) Проверяет правильность введенных пользователем данных.
    3) Возвращает пользовательские данные в замаскированном формате."""

    # Код ниже выполняет работу с номером банковской карты.
    user_input_card = input("Введите номер карты: ").strip()
    correct_card = check_user_input(user_input_card, LENGTH_OF_CARD_NUMBER)
    mask_card_number = get_mask_card_number(correct_card)

    # Код ниже выполняет работу с номером банковского счета.
    user_input_account = input("Введите номер счета: ").strip()
    correct_account = check_user_input(user_input_account, LENGTH_OF_ACCOUNT_NUMBER)
    mask_account_number = get_mask_account(correct_account)

    # Ниже вывод готового результата.
    print(mask_card_number, mask_account_number, sep="\n")


if __name__ == "__main__":
    main()
