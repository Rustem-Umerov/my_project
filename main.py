from src.widget import output_result


def main() -> None:
    """Данная функция выполняет:
    - Принимает от пользователя данные (номер банковской карты и номер банковского счета).
    Далее передает пользовательские данные в функцию, которая:
    - Проверяет правильность введенных пользователем данных.
    - Возвращает пользовательские данные в замаскированном формате."""

    # Код ниже выполняет работу с номером банковской карты.
    user_input = input("Введите счет или название и номер карты: ").strip()
    mask_result = output_result(user_input)

    # Ниже вывод готового результата.
    print(mask_result)


if __name__ == "__main__":
    main()
