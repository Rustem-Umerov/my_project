from src.widget import output_result


def main() -> None:
    """Принимает данные (карта или счёт), проверяет их и возвращает замаскированные.

    - Запрашивает данные у пользователя
    - Проверяет формат:
      * Для карт: "Имя 16_цифр"
      * Для счетов: "счёт 20_цифр"
    - Возвращает замаскированные данные или ошибку при неверном формате
    """

    while True:

        try:
            user_input = input("Введите счет и номер счета или название и номер карты: ").strip().title()
            mask_result = output_result(user_input)

            print(mask_result)

        except ValueError as e:
            print(e)

        finally:
            user_input = input("""Желаете повторить???
            Если да - введите 'да': """).strip().lower()

            if user_input != "да":
                break


if __name__ == "__main__":
    main()
