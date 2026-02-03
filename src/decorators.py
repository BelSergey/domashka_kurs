from typing import Optional, Any, Callable
import functools


def log(filename: Optional[str] = None):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            pass

        return wrapper()

    return decorator()

