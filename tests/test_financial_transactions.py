from pathlib import Path
from typing import Any
from unittest.mock import Mock, mock_open, patch

import pytest
from pytest import LogCaptureFixture

from src.financial_transactions import detect_delimiter


def fake_sniff(_sample: str, _delimiters: str) -> Any:
    """
    Функция, которая заменяет csv.Sniffer.sniff().
    Она возвращает mock-объект с атрибутом delimiter, равным ';'
    """
    mock_dialect = Mock()
    mock_dialect.delimiter = ";"
    return mock_dialect


def test__detect_delimiter_correct_delimiter() -> None:
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
def test__detect_delimiter_correct_delimiter_log_message(caplog: LogCaptureFixture, log_message: str) -> None:
    """Тест проверяет логирование ошибок."""

    fake_data = "apple1;apple2;apple3\napple4;apple5;apple6\napple7;apple8;apple9"
    fake_path = Path("fake_transactions.csv")
    with patch("builtins.open", new_callable=mock_open, read_data=fake_data):
        detect_delimiter(fake_path)

    assert log_message in caplog.text


def test__detect_delimiter_file_not_found(caplog: LogCaptureFixture) -> None:
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


def test__detect_delimiter_except_exception(caplog: LogCaptureFixture) -> None:
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
