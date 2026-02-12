import datetime
import functools
import os
from typing import Any, Callable, Optional


def write_log(message: str, filename: Optional[str] = None) -> None:
    """Запись лога в файл (если имя корректное) или в консоль."""
    if filename and filename.strip():
        dirname = os.path.dirname(filename.strip())
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)
        with open(filename.strip(), "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования вызовов функций."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Актуальный файл лога: приоритет у параметра, затем переменная окружения
            log_file = filename if filename is not None else os.getenv("LOG_FILE_PATH")

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_name = func.__name__

            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
            signature = ",".join(args_repr + kwargs_repr)

            try:
                result = func(*args, **kwargs)
                end_timestamp = timestamp
                msg = (
                    f"[{end_timestamp}] Функция {func_name} вызвана с аргументами ({signature}) -> "
                    f"результат: {repr(result)}"
                )
                write_log(msg, log_file)
                return result
            except Exception as e:
                error_timestamp = timestamp
                error_msg = (
                    f"[{error_timestamp}] Ошибка в функции {func_name}({signature}): " f"{type(e).__name__}: {e}"
                )
                write_log(error_msg, log_file)
                raise

        return wrapper

    return decorator
