from pathlib import Path
from typing import Any
from unittest.mock import Mock, mock_open, patch

import pandas as pd
import pytest
from pandas.errors import ParserError
from pytest import LogCaptureFixture

from src.financial_transactions import (detect_delimiter, fin_trans_from_csv_file, fin_trans_from_excel_file,
                                        validate_transactions_list)


def fake_sniff(sample: str, delimiters: str) -> Any:
    """
    Функция, которая заменяет csv.Sniffer.sniff().
    Она возвращает mock-объект с атрибутом delimiter, равным ';'
    """
    mock_dialect = Mock()
    mock_dialect.delimiter = ";"
    return mock_dialect


def test_detect_delimiter_correct_delimiter() -> None:
    """Тестирует успешное определение разделителя."""

    # Ниже пример файла для теста. Данные с разделителем ";".
    fake_data = "apple1;apple2;apple3\napple4;apple5;apple6\napple7;apple8;apple9"
    fake_path = Path("fake_transactions.csv")

    # Ниже патчу open, чтобы заменить обращение к файловой системе. И сразу патчу метод sniff,
    # чтобы вернуть наш тестовый объект.
    with (
        patch("builtins.open", new_callable=mock_open, read_data=fake_data) as mock_file,
        patch("csv.Sniffer.sniff", side_effect=fake_sniff) as mock_sniff,
    ):

        # Вызываю функцию _detect_delimiter и передаю в нее fake_path.
        detected_delimiter = detect_delimiter(fake_path)

        assert detected_delimiter == ";"

        # Проверяю, что open был вызван с нужными аргументами.
        mock_file.assert_called_once_with(fake_path, "r", encoding="utf-8")

        # Образец данных для sniff. Вывожу первые 1024 байта из fake_data.
        expected_sample = fake_data[:1024]
        mock_sniff.assert_called_once_with(expected_sample, delimiters=";,\t|")


@pytest.mark.parametrize(
    "log_message",
    [
        "Образец данных из файла прочитан",
        "Определен разделитель:",
    ],
)
def test_detect_delimiter_correct_delimiter_log_message(caplog: LogCaptureFixture, log_message: str) -> None:
    """Тест проверяет логирование ошибок."""

    fake_data = "apple1;apple2;apple3\napple4;apple5;apple6\napple7;apple8;apple9"
    fake_path = Path("fake_transactions.csv")
    with patch("builtins.open", new_callable=mock_open, read_data=fake_data):
        detect_delimiter(fake_path)

    assert log_message in caplog.text


def test_detect_delimiter_file_not_found(caplog: LogCaptureFixture) -> None:
    """
    Тест тестирует ситуацию, когда файл не найден.

    Патчу open так, чтобы он выбрасывал FileNotFoundError,
    и проверяю, что функция видит это исключение.

    Далее тест проверяет логирование ошибок.
    """

    fake_path = Path("fake_transactions.csv")
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            detect_delimiter(fake_path)

        assert "Файл", "не найден!" in caplog.text


def test_detect_delimiter_except_exception(caplog: LogCaptureFixture) -> None:
    """Тест проверят, что функция корректно обрабатывает исключение Exception."""

    fake_data = "не правильные данные, для того чтобы было вызвано except Exception as e"
    fake_path = Path("fake_transactions.csv")

    with (
        patch("builtins.open", new_callable=mock_open, read_data=fake_data),
        patch("csv.Sniffer.sniff", side_effect=Exception("Error: fake error for testing")),
    ):

        with pytest.raises(Exception) as exception_info:
            detect_delimiter(fake_path)

    assert "Error: fake error for testing" in str(exception_info.value)
    assert "Неизвестная ошибка при чтении" in caplog.text


@pytest.mark.parametrize(
    "log_message",
    [
        "Происходит открытие CSV-файла:",
        "CSV-файл успешно открыт. Информация из файла получена.",
    ],
)
def test_fin_trans_from_csv_file_correct_file_and_log_message(caplog: LogCaptureFixture, log_message: str) -> None:
    """Тест проверяет:
    - корректное выполнение функции при корректном считывании CSV-файла.
    - правильный вывод логов."""

    # Ниже список словарей для теста.
    fake_data = [
        {"fruit1": "apple1", "fruit2": "apple2", "fruit3": "apple3"},
        {"fruit1": "apple4", "fruit2": "apple5", "fruit3": "apple6"},
        {"fruit1": "apple7", "fruit2": "apple8", "fruit3": "apple9"},
    ]

    fake_path = Path("fake_transactions.csv")  # имитация пути к файлу.
    expected_delimiter = ";"  # ожидаемый разделитель.

    fake_data_frame = pd.DataFrame(fake_data)  # преобразую список словарей в объект DataFrame.
    expected_result = fake_data_frame.to_dict(orient="records")  # перевожу объект DataFrame в список.

    with (
        patch("src.financial_transactions.detect_delimiter", return_value=expected_delimiter) as mock_detect,
        patch("src.financial_transactions.pd.read_csv", return_value=fake_data_frame) as mock_read_csv,
        patch("src.financial_transactions.validate_transactions_list") as mock_validate,
    ):
        result = fin_trans_from_csv_file(fake_path)  # вызов функции.

        assert result == expected_result  # проверка результата.

        # ниже проверка того, что каждая функция вызывалась с нужными параметрами.
        mock_detect.assert_called_once_with(fake_path)
        mock_read_csv.assert_called_once_with(fake_path, sep=expected_delimiter, encoding="utf-8")
        mock_validate.assert_called_once_with(fake_data, fake_path)

        assert log_message in caplog.text  # проверка логов.


def test_fin_trans_from_csv_file_file_not_found(caplog: LogCaptureFixture) -> None:
    """
    Тест проверяет, что при отсутствии файла функция:
    - регистрирует ошибку и выбрасывает исключение FileNotFoundError.
    - выводит правильное логирование."""

    fake_path = Path("fake_transactions.csv")  # имитация пути к файлу.
    expected_delimiter = ";"  # ожидаемый разделитель.

    with (
        patch("src.financial_transactions.detect_delimiter", return_value=expected_delimiter),
        patch("src.financial_transactions.pd.read_csv", side_effect=FileNotFoundError("File not found")),
        pytest.raises(FileNotFoundError) as exc_info,
    ):

        fin_trans_from_csv_file(fake_path)

    assert "File not found" in str(exc_info)

    assert "Файл", "не найден!" in caplog.text


def test_fin_trans_from_csv_file_parser_error(caplog: LogCaptureFixture) -> None:
    """
    Тест проверяет, что при возникновении ошибки парсинга CSV функция:
    - регистрирует ошибку и выбрасывает исключение pd.errors.ParserError.
    - выводит правильное логирование"""
    fake_path = Path("fake_transactions.csv")

    with (
        patch("src.financial_transactions.detect_delimiter", return_value=";"),
        patch("src.financial_transactions.pd.read_csv", side_effect=ParserError("Ошибка парсинга")),
    ):
        with pytest.raises(ParserError) as exc_info:
            fin_trans_from_csv_file(fake_path)

    assert "Ошибка парсинга" in str(exc_info.value)
    assert "Ошибка в CSV-файле" in caplog.text


def test_fin_trans_from_csv_file_unknown_exception(caplog: LogCaptureFixture) -> None:
    """
    Тест проверяет поведение функции при возникновении неизвестной ошибки:
    - вызывается общее исключение Exception.
    - проверяется, что ошибка залогирована.
    """
    fake_path = Path("fake_transactions.csv")

    with (
        patch("src.financial_transactions.detect_delimiter", return_value=";"),
        patch("src.financial_transactions.pd.read_csv", side_effect=Exception("Неожиданная ошибка")),
    ):
        with pytest.raises(Exception) as exc_info:
            fin_trans_from_csv_file(fake_path)

    assert "Неожиданная ошибка" in str(exc_info.value)
    # Если в логах присутствует фраза "Неизвестная ошибка при чтении", проверим её
    assert "Неизвестная ошибка при чтении" in caplog.text


def test_fin_trans_from_excel_correct_file() -> None:
    """
    Тест проверяет корректное выполнение функции при корректно чтении Excel-файла.
    Используются патчи для pd.read_excel и validate_transactions_list.
    """
    fake_path = Path("fake_transactions.xlsx")
    # Пример списка со словарями транзакций.
    fake_data = [
        {"operation1": "A", "operation2": "B", "operation3": "C"},
        {"operation1": "D", "operation2": "E", "operation3": "F"},
    ]
    # Создаю DataFrame из fake_data.
    fake_data_frame = pd.DataFrame(fake_data)
    expected_result = fake_data_frame.to_dict(orient="records")  # перевожу DataFrame в список словарей

    with (
        patch("src.financial_transactions.pd.read_excel", return_value=fake_data_frame) as mock_read_excel,
        patch("src.financial_transactions.validate_transactions_list") as mock_validate,
    ):
        result = fin_trans_from_excel_file(fake_path)

        # Сравниваю готовые списки.
        assert result == expected_result

        # Проверяю вызовы функций с нужными параметрами.
        mock_read_excel.assert_called_once_with(fake_path)
        mock_validate.assert_called_once_with(expected_result, fake_path)


@pytest.mark.parametrize(
    "log_message", ["Происходит открытие Excel-файла:", "Excel-файл успешно открыт. Информация из файла получена."]
)
def test_fin_trans_from_excel_correct_file_log_message(caplog: LogCaptureFixture, log_message: str) -> None:
    """Тест проверяет, что при успешном чтении Excel-файла в логах присутствуют нужные сообщения."""

    fake_path = Path("fake_transactions.xlsx")
    # Пример списка со словарями транзакций.
    fake_data = [
        {"operation1": "A", "operation2": "B", "operation3": "C"},
        {"operation1": "D", "operation2": "E", "operation3": "F"},
    ]
    # Создаю DataFrame из fake_data.
    fake_data_frame = pd.DataFrame(fake_data)

    with (
        patch("src.financial_transactions.pd.read_excel", return_value=fake_data_frame),
        patch("src.financial_transactions.validate_transactions_list"),
    ):
        caplog.clear()
        fin_trans_from_excel_file(fake_path)

    assert log_message in caplog.text


def test_fin_trans_from_excel_file_file_not_found(caplog: LogCaptureFixture) -> None:
    """
    Тест проверяет, что при отсутствии Excel-файла функция логирует ошибку и выбрасывает FileNotFoundError.
    """
    fake_path = Path("nonexistent.xlsx")

    with (
        patch("src.financial_transactions.pd.read_excel", side_effect=FileNotFoundError("File not found")),
        pytest.raises(FileNotFoundError) as exc_info,
    ):
        fin_trans_from_excel_file(fake_path)

    assert "File not found" in str(exc_info.value)
    assert "Файл", "не найден!" in caplog.text


def test_fin_trans_from_excel_file_parser_error(caplog: LogCaptureFixture) -> None:
    """
    Тест проверяет, что при возникновении ошибки парсинга Excel-файла функция логирует ошибку и выбрасывает ParserError.
    """
    fake_path = Path("fake_transactions.xlsx")

    with (
        patch("src.financial_transactions.pd.read_excel", side_effect=ParserError("Ошибка парсинга")),
        pytest.raises(ParserError) as exc_info,
    ):
        fin_trans_from_excel_file(fake_path)

    assert "Ошибка парсинга" in str(exc_info.value)
    assert "Ошибка при парсинге Excel-файла" in caplog.text


def test_validate_transactions_list(caplog: LogCaptureFixture) -> None:
    """
    Если список транзакций пуст, функция должна залогировать сообщение и выбросить ValueError.
    """
    fake_path = Path("fake_transactions.csv")
    with pytest.raises(ValueError) as exc_info:
        validate_transactions_list([], fake_path)

    # Ниже проверяю, что текст исключения содержит указание на отсутствие данных
    assert "Файл", "не содержит данных" in str(exc_info.value)
    # Проверяем, что в логах содержится соответствующее сообщение
    assert "Файл", "не содержит данных" in caplog.text


def test_validate_transactions_list_non_empty_list() -> None:
    """
    Если список транзакций не пуст, функция не должна выбрасывать исключения.
    """
    fake_path = Path("fake_transactions.csv")
    transactions = [{"operation": 1, "amount": 100}, {"operation": 2, "amount": 200}]

    # Ниже функция возвращает не выбрасывает исключения, так как список не пустой.
    validate_transactions_list(transactions, fake_path)
