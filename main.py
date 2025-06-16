from pathlib import Path

from src.banking_operations import process_bank_search
from src.financial_transactions import fin_trans_from_csv_file, fin_trans_from_excel_file
from src.generators import filter_by_currency
from src.logger_config import get_logger
from src.processing import filter_by_state, sort_by_date
from src.utils import financial_operations
from src.widget import get_date, mask_account_card

BASE_DIR = Path(__file__).resolve()
JSON_PATH = BASE_DIR.parent / "data" / "operations.json"
CSV_PATH = BASE_DIR.parent / "data" / "transactions.csv"
XLSX_PATH = BASE_DIR.parent / "data" / "transactions_excel.xlsx"

LOAD_FILE = {
    1: lambda: financial_operations(JSON_PATH),
    2: lambda: fin_trans_from_csv_file(CSV_PATH),
    3: lambda: fin_trans_from_excel_file(XLSX_PATH),
}

VALID_STATUSES = ["EXECUTED", "CANCELED", "PENDING"]

logger = get_logger(
    __name__,
    level="DEBUG",
    log_file="main.log",
    fmt="%(asctime)s - %(module)s - %(levelname)s - %(message)s",
    mode="w",
)


def main() -> None:
    """
    Программа для работы с банковскими транзакциями.

    Функциональность:
      - Выбор источника данных:
            * JSON-файл (файл operations.json)
            * CSV-файл (файл transactions.csv)
            * XLSX-файл (файл transactions_excel.xlsx)
      - Фильтрация транзакций по статусу (EXECUTED, CANCELED, PENDING)
      - Сортировка транзакций по дате по выбранному порядку (по возрастанию/по убыванию),
        при этом сортировка является опциональной.
      - Фильтрация по валюте (вывод только транзакций в рублях, если указано).
      - Фильтрация по ключевому слову в описании транзакции (при необходимости).
      - Вывод итогового списка транзакций с информацией о дате, описании, счетах и сумме.
    """

    logger.info("Программа выводит меню.")
    print()
    print(
        """Привет! Добро пожаловать в программу работы с банковскими транзакциями.""")
    print()
    print(
        """Выберите необходимый пункт меню:
    1. Получить информацию о транзакциях из JSON-файла
    2. Получить информацию о транзакциях из CSV-файла
    3. Получить информацию о транзакциях из XLSX-файла
    """
    )

    while True:
        user_input = input().strip()
        if user_input.isdigit() and 1 <= int(user_input) <= 3:
            user_input_int: int = int(user_input)
            break
        print("Ошибка: нужно ввести число от 1 до 3.")

    if user_input_int == 1:
        print("Для обработки выбран JSON-файл.")
        logger.info("Для обработки выбран JSON-файл.")
    elif user_input_int == 2:
        print("Для обработки выбран CSV-файл.")
        logger.info("Для обработки выбран CSV-файл.")
    else:
        print("Для обработки выбран XLSX-файл.")
        logger.info("Для обработки выбран XLSX-файл.")

    operations_list = LOAD_FILE[user_input_int]()
    logger.info("Программа считала информацию из файла.")

    logger.info("Программа просит пользователя выбрать статус для фильтрации.")
    while True:
        print(
            """
Введите статус, по которому необходимо выполнить фильтрацию. 
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING
""")
        user_status = input().strip()
        user_status_upper = user_status.upper()
        print()

        if user_status_upper in VALID_STATUSES:
            print(f'Операции отфильтрованы по статусу "{user_status_upper}"')
            operations_list = filter_by_state(operations_list, user_status_upper)
            logger.info("Пользователь выбрал статус %s. Операции отфильтрованы по статусу.", user_status)
            break
        else:
            print(f"Статус операции '{user_status}' недоступен.")

    logger.info("Программа спрашивает у пользователя: Отсортировать операции по дате(Да/Нет)?")
    while True:
        print()
        print("Отсортировать операции по дате? Да/Нет")
        print()
        user_data_input = input().strip().lower()
        if user_data_input == "да":

            logger.info("Пользователь хочет отсортировать операции по дате.")
            print()
            print("Отсортировать по возрастанию или по убыванию?")
            print()
            user_sorted_input = input().strip()
            if user_sorted_input.lower() == "по возрастанию":
                operations_list = sort_by_date(operations_list, False)
                logger.info("Программа отсортировала операции по возрастанию.")
                break
            elif user_sorted_input.lower() == "по убыванию":
                operations_list = sort_by_date(operations_list)
                logger.info("Программа отсортировала операции по убыванию.")
                break
            else:
                print("Вы ввели неверный ответ. Повторите попытку.")

        elif user_data_input == "нет":
            logger.info("Пользователь отвечает: 'Нет'.")
            break
        else:
            print("Вы ввели неверный ответ. Повторите попытку.")

    logger.info("Программа спрашивает у пользователя: Выводить только рублевые транзакции(Да/Нет)?")
    while True:
        print()
        print("Выводить только рублевые транзакции? Да/Нет")
        print()
        user_currency_input = input().strip()
        if user_currency_input.lower() == "да":
            operations_list = list(filter_by_currency(operations_list, "RUB"))
            logger.info("Пользователь выбирает, вывод только рублевых транзакции.")
            break
        elif user_currency_input.lower() == "нет":
            logger.info("Пользователь выбирает, вывод всех транзакции.")
            break
        else:
            print("Вы ввели неверный ответ. Повторите попытку.")

    logger.info(
    "Программа спрашивает у пользователя: Отфильтровать список транзакций по определенному слову в описании(Да/Нет)?"
    )
    while True:
        print()
        print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
        print()
        user_input_filter_word = input().strip()
        if user_input_filter_word.lower() in ["да", "нет"]:
            if user_input_filter_word == "да":
                print()
                keyword = input("Введите слово для фильтрации: ").strip()
                print(f"Фильтрация по слову: {keyword}")
                operations_list = process_bank_search(operations_list, keyword)
                logger.info("Пользователь ввел слово для фильтрации: %s", keyword)
                break
            else:
                logger.info("Пользователь отказался фильтровать список транзакций по определенному слову в описании.")
                break

        print("Вы ввели неверный ответ. Повторите попытку.")

    print()
    print("Распечатываю итоговый список транзакций...")
    logger.info("Программа распечатывает итоговый список транзакций.")

    if not operations_list:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        logger.info("Программа не нашла ни одной транзакции, подходящей под условия фильтрации.")

    else:
        print(f"Всего банковских операций в выборке: {len(operations_list)}")
        logger.info("Всего банковских операций в выборке: %s", len(operations_list))

        for transaction in operations_list:
            description: str = transaction.get("description", "")
            date_str: str = transaction.get("date", "")
            to_account: str = transaction.get("to", "")

            # Вывод информации для открытия вклада
            if description.lower() == "открытие вклада":

                date = get_date(date_str)
                account = mask_account_card(to_account)
                if "operationAmount" in transaction:
                    amount = transaction.get("operationAmount", {}).get("amount")
                    currency_name = transaction.get("operationAmount", {}).get("currency", {}).get("name")
                else:
                    amount = transaction.get("amount")
                    currency_name = transaction.get("currency_name")

                print(f"{date} {description}\n" f"{account}\n" f"Сумма: {amount} {currency_name}")

            else:
                from_account: str = transaction.get("from", "")

                date = get_date(date_str)
                from_transfer = mask_account_card(from_account)
                to_transfer = mask_account_card(to_account)

                if "operationAmount" in transaction:
                    amount = transaction.get("operationAmount", {}).get("amount")
                    currency_name = transaction.get("operationAmount", {}).get("currency", {}).get("name")
                else:
                    amount = transaction.get("amount")
                    currency_name = transaction.get("currency_name")

                print(
                    f"{date} {description}\n" f"{from_transfer} -> {to_transfer}\n" f"Сумма: {amount} {currency_name}"
                )

            print()


if __name__ == "__main__":
    main()
