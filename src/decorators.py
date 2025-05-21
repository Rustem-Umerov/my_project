from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from src.logger_config import get_logger

T = TypeVar("T")
P = ParamSpec("P")


def log(filename: str | None = None) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Декоратор, который логирует:
      - начало выполнения функции;
      - переданные позиционные и именованные аргументы;
      - успешное завершение с результатом.

    В случае, если возникнет исключение:
      - исключение, если оно возникает, с типом и трассировкой.

    :param filename: Опциональный путь к файлу логов. Если указан, логи будут записываться в файл;
                     в противном случае логи будут выводиться в консоль.
    :return: Декоратор, который можно применить к любой функции.
    """

    def my_decorator(func: Callable[P, T]) -> Callable[P, T]:

        module_name = getattr(func, "__module__", __name__)
        logger = get_logger(module_name, log_file=filename)

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            """Обертка для декорируемой функции"""

            logger.info("Starting function %s with arguments: args=%s, kwargs=%s", func.__name__, args, kwargs)

            try:
                result = func(*args, **kwargs)
                logger.info("Function %s completed successfully. Result: %s", func.__name__, result)
                return result

            except Exception as e:
                logger.exception(
                    "Error in function %s. Error type: %s. Arguments: args=%s, kwargs=%s",
                    func.__name__,
                    type(e).__name__,
                    args,
                    kwargs,
                )
                raise

        return wrapper

    return my_decorator
