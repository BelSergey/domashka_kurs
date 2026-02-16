
class Calculator:
    """Класс калькулятора для тестирования декораторов на методах."""

    def __init__(self) -> None:
        """Инициализирует калькулятор с нулевой памятью."""
        self.memory = 0

    def add(self, a: int, b: int) -> int:
        """Складывает два числа."""
        return a + b

    def subtract(self, a: int, b: int) -> int:
        """Вычитает второе число из первого."""
        return a - b

    def multiply(self, a: int, b: int) -> int:
        """Умножает два числа."""
        return a * b

    def divide(self, a: int, b: int) -> float:
        """Делит первое число на второе."""
        return a / b
