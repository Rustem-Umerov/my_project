import csv
from pathlib import Path

import pandas as pd

from src.logger_config import get_logger

logger = get_logger(__name__)

my_project_dir = Path(__file__).resolve().parent.parent
csv_file_path = my_project_dir / "files_with_financ_transactions" / "transactions.csv"


def _detect_delimiter(file_path: Path, sample_size: int = 1024) -> str:
    """Функция определяет разделитель в CSV-файле с помощью csv.Sniffer"""

    try:
        logger.info("Анализ разделителя в файле: %s", file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            sample = f.read(sample_size)
            logger.info("Образец данных из файла прочитан (первые %s байт).", sample_size)

            # Ниже создаю объект sniffer класса csv.Sniffer()
            sniffer = csv.Sniffer()
            # Вызываю метод sniff(): Метод анализирует строку sample, учитывая список кандидатов на разделители ;,\t|
            dialect = sniffer.sniff(sample, delimiters=";,\t|")
            # Ниже извлекаю найденный разделитель
            detected_delimiter = dialect.delimiter
            logger.info("Определен разделитель: %s", detected_delimiter)

            return detected_delimiter

    except FileNotFoundError:
        logger.error("Файл %s не найден!", file_path)
        raise
    except Exception as e:
        logger.error("Неизвестная ошибка при чтении %s: %s", file_path, str(e))
        raise


def fin_trans_from_csv_file(file_path: Path) -> list[dict]:
    """Функция для считывания финансовых операций из CSV-файла.
    Принимает путь к файлу CSV в качестве аргумента.
    Возвращает список словарей с транзакциями."""

    try:
        logger.info("Происходит открытие CSV-файла: %s", file_path)
        delimiter = _detect_delimiter(file_path)

        df = pd.read_csv(file_path, sep=delimiter, encoding="utf-8")
        logger.info("CSV-файл успешно открыт. Информация из файла получена.")

        transactions_list = df.to_dict(orient="records")

        if not transactions_list:
            logger.info("Файл %s не содержит данных", file_path)
            raise ValueError("Файл %s не содержит данных", file_path)

        return transactions_list

    except FileNotFoundError:
        logger.error("Файл %s не найден!", file_path)
        raise
    except pd.errors.ParserError as e:
        logger.error("Ошибка в CSV-файле %s: %s", file_path, str(e))
        raise
    except Exception as e:
        logger.error("Неизвестная ошибка при чтении %s: %s", file_path, str(e))
        raise
