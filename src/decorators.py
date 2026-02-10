import datetime
import functools
import os
from typing import Any, Callable, Optional, Union

from dotenv import load_dotenv

load_dotenv()
LOG_FILE = os.getenv("LOG_FILE_PATH")


def log( func: Optional[Callable] = None, filename: Optional[str] = None
) -> Union[Callable, Callable[[Callable], Callable]]:
    def decorator(actual_func: Callable) -> Callable:
        @functools.wraps(actual_func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if filename is not None:
                log_file = filename
            elif LOG_FILE is not None:
                log_file = LOG_FILE

            time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_name = actual_func.__name__

            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
            signature = ",".join(args_repr + kwargs_repr)

            start_message = f"[{time_stamp}] Начало выполнения {func_name} ({signature})"
            write_log(start_message, log_file)
            try:
                result = actual_func(*args, **kwargs)
                end_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                end_msg = f"[{end_timestamp}] Функция {func_name} успешно выполнена. "
                write_log(end_msg, log_file)
                return result
            except Exception as e:
                error_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                error_message = (
                    f"[{error_timestamp}] Ошибка в функции {func_name}({signature}): {type(e).__name__}: {str(e)}"
                )
                write_log(error_message, log_file)
                raise

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)


def write_log(message: str, filename: Optional[str] = None) -> None:
    """Функция для записи логов в файл или консоль"""
    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)
