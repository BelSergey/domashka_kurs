import logging
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "calculator.log"

LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)


class Calculator:
    """Калькулятор с логированием вызовов методов."""

    def __init__(self) -> None:
        """Инициализация калькулятора."""
        self.memory = 0
        logger.info("Создан экземпляр Calculator")

    def add(self, a: int, b: int) -> int:
        """Сложение двух чисел."""
        logger.debug(f"Вызов add с аргументами a={a}, b={b}")
        try:
            result = a + b
            logger.debug(f"Результат add: {result}")
            return result
        except Exception as e:
            logger.exception("Ошибка в методе add")
            raise

    def subtract(self, a: int, b: int) -> int:
        """Вычитание."""
        logger.debug(f"Вызов subtract с аргументами a={a}, b={b}")
        try:
            result = a - b
            logger.debug(f"Результат subtract: {result}")
            return result
        except Exception as e:
            logger.exception("Ошибка в методе subtract")
            raise

    def multiply(self, a: int, b: int) -> int:
        """Умножение."""
        logger.debug(f"Вызов multiply с аргументами a={a}, b={b}")
        try:
            result = a * b
            logger.debug(f"Результат multiply: {result}")
            return result
        except Exception as e:
            logger.exception("Ошибка в методе multiply")
            raise

    def divide(self, a: int, b: int) -> float:
        """Деление. Логируем попытку деления на ноль."""
        logger.debug(f"Вызов divide с аргументами a={a}, b={b}")
        try:
            if b == 0:
                logger.error("Попытка деления на ноль")
                raise ZeroDivisionError("Деление на ноль недопустимо")
            result = a / b
            logger.debug(f"Результат divide: {result}")
            return result
        except ZeroDivisionError:
            logger.exception("Деление на ноль")
            raise
        except Exception as e:
            logger.exception("Ошибка в методе divide")
            raise