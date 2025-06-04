import re
from pathlib import Path

from src.logger_config import get_logger

LENGTH_OF_CARD_NUMBER = 16  # Константа указывающая длину номера банковской карты
LENGTH_OF_ACCOUNT_NUMBER = 20  # Константа указывающая длину номера банковского счета

logs_dir = Path(__file__).resolve().parent.parent / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)  # Создаем директорию, если отсутствует
logs_file = logs_dir / "masks.log"

logger = get_logger(
    __name__,
    level="DEBUG",
    log_file=str(logs_file),
    fmt="%(asctime)s - %(module)s - %(levelname)s - %(message)s",
    mode="w",
)


def is_account(text: str) -> bool:
    """Проверяет, начинается ли строка на сч[её]т."""

    logger.debug("Вход в is_account с текстом: %s", text)
    result = bool(re.match(r"сч[её]т", text, re.IGNORECASE))
    logger.debug("Результат is_account: %s", result)
    return result


def check_user_input(user_input: str) -> bool:
    """Функция проверяет входные данные от пользователя."""

    logger.debug("Вход в check_user_input. Данные: %s", user_input)

    if is_account(user_input):
        pattern = rf"^([a-zA-Zа-яёА-ЯЁ]+\s?){{1,2}}\d{{{LENGTH_OF_ACCOUNT_NUMBER}}}\b"
        logger.debug("Обнаружен ввод для счета. Применяется паттерн для счета.")
    else:
        pattern = rf"^([a-zA-Zа-яёА-ЯЁ]+\s?){{1,2}}\d{{{LENGTH_OF_CARD_NUMBER}}}\b"
        logger.debug("Обнаружен ввод для карты. Применяется паттерн для карты.")

    result = bool(re.fullmatch(pattern, user_input))
    logger.debug("Результат проверки check_user_input: %s", result)
    return result


def get_mask_card_number(card_number: str) -> str:
    """Принимает номер карты. Возвращает в замаскированном виде.
    Видны первые 6 цифр и последние 4 цифры, остальные символы отображаются звездочками,
    номер разбит по блокам по 4 цифры, разделенным пробелами."""

    logger.debug("Начато маскирование номера карты. Будут видны первые 6 и последние 4 цифры.")
    result_masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"
    logger.debug("Маскирование номера карты завершено: %s", result_masked)
    return result_masked


def get_mask_account(account_number: str) -> str:
    """Принимает на вход номер счета и возвращает его замаскированный вид.
    Видны только последние 4 цифры номера, а перед ними — две звездочки"""

    logger.debug("Начато маскирование номера счета. Будут видны последние 4 цифры.")
    result_masked = f"**{account_number[-4:]}"
    logger.debug("Маскирование номера счета завершено: %s", result_masked)
    return result_masked


def error_message() -> str:
    """Функция выводит сообщение об ошибке, если пользователь
    ввел не верные данные."""

    logger.error("Функция error_message вызвана: неверные данные от пользователя.")
    return f"""
            *** Ошибка - Вы ввели неверные данные ***
        Введите данные в таком формате:
        <<"название карты или счета" "номер карты или счета">>
        Номер карты {LENGTH_OF_CARD_NUMBER} цифр, номер счета {LENGTH_OF_ACCOUNT_NUMBER} цифр.
        """
