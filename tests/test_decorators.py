import pytest
from _pytest.capture import CaptureFixture
from _pytest.logging import LogCaptureFixture

from src.decorators import log


def test_returns_result(capsys: CaptureFixture[str]) -> None:
    """Данный тест проверяет вывод правильного результата."""

    @log(filename=None)
    def addition(a: float, b: float) -> float:
        """Дополнительная функция, необходимая для тестирования вывода правильного результата."""

        return a + b

    result = addition(5, 5)

    assert result == 10


def test_return_exception(capsys: CaptureFixture[str]) -> None:
    """Данный тест проверяет вывод исключения."""

    @log(filename=None)
    def division(a: float, b: float) -> float:
        """Дополнительная функция, необходимая для тестирования вывода исключения."""

        return a / b

    with pytest.raises(Exception):
        assert division(5, 0)


def test_return_correct_text(capsys: CaptureFixture[str]) -> None:
    """Данный тест проверяет вывод корректного текста."""

    def greeting() -> None:
        """Дополнительная функция, необходимая для тестирования вывода корректного текста."""

        print("Hello world!")

    greeting()
    captured = capsys.readouterr()
    assert "Hello world!" in captured.out


# Ниже дополнительная функция для тестирования логов.
@log(filename=None)
def add(a: float, b: float) -> float:
    """Дополнительная функция, необходимая для тестирования логов из декоратора."""

    return a + b


def test_add(caplog: LogCaptureFixture) -> None:
    """Данный тест проверяет, что декоратор возвращает правильные логи,
    в том случае, если функция успешно выполнена."""

    with caplog.at_level("INFO"):
        result = add(5, 5)

        assert result == 10  # Проверка правильного результата.

        # Проверка логов.
        assert "Starting function add with arguments: args=(5, 5), kwargs={}" in caplog.text
        assert "Function add completed successfully. Result: 10" in caplog.text

        # Проверяем, есть ли лог-записи с уровнем INFO.
        exception_records = [record for record in caplog.records if record.levelname == "INFO"]
        assert exception_records, "Нет логов уровня INFO"


# Ниже дополнительная функция для тестирования логов.
@log(filename=None)
def divide(a: float, b: float) -> float:
    """Дополнительная функция, необходимая для тестирования логов из декоратора."""

    return a / b


def test_divide_error(caplog: LogCaptureFixture) -> None:
    """Данный тест проверяет, что декоратор возвращает правильные логи,
    в том случае, если возникает ошибка."""

    caplog.clear()  # Очистка предыдущих логов, если они присутствуют.
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)

    # Проверка логов.
    assert "Starting function divide with arguments: args=(5, 0), kwargs={}" in caplog.text
    assert "Error in function divide. Error type: ZeroDivisionError. Arguments: args=(5, 0), kwargs={}" in caplog.text

    # Проверяем, есть ли лог-записи с уровнем INFO.
    exception_records = [record for record in caplog.records if record.levelname == "INFO"]
    assert exception_records, "Нет логов уровня INFO"

    # Проверяем, есть ли лог-записи с уровнем ERROR (так как logger.exception создает запись с уровнем ERROR).
    exception_records = [record for record in caplog.records if record.levelname == "ERROR"]
    assert exception_records, "Нет логов уровня ERROR"
