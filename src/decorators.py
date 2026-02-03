from typing import Optional, Any, Callable
import functools


def log(filename: Optional[str] = None):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            pass

        return wrapper()

    return decorator()

def write_log (message: str, filename: Optional[str] = None) -> None:
    """Функция для записи логов в файл или консоль"""
    if filename:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(message + '\n')
    else: print(message)