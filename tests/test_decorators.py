import os
from typing import Any, Callable, Optional

import pytest

from src.decorators import log, write_log
from src.utils.simple_calculator import Calculator


def _factorial(n: int) -> int:
    """Рекурсивная функция факториала, определённая на уровне модуля."""
    if n <= 1:
        return 1
    return n * _factorial(n - 1)


def test_write_log_creates_file(temp_file_path: str) -> None:
    """Проверяет, что write_log создает файл и записывает сообщение."""
    test_message = "Тестовое сообщение"
    write_log(test_message, temp_file_path)
    assert os.path.exists(temp_file_path)
    with open(temp_file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    assert content == test_message


def test_write_log_to_console(capture_output: Callable[[], str]) -> None:
    """Проверяет, что write_log выводит в консоль при filename=None."""
    test_message = "Вывод в консоль"
    write_log(test_message, None)
    output = capture_output()
    assert test_message in output


def test_write_log_appends(temp_file_path: str) -> None:
    """Проверяет, что write_log добавляет текст в конец файла."""
    write_log("Первая строка", temp_file_path)
    write_log("Вторая строка", temp_file_path)
    with open(temp_file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    assert len(lines) == 2
    assert lines[0] == "Первая строка"
    assert lines[1] == "Вторая строка"


def test_write_log_with_whitespace_filename(capture_output: Callable[[], str]) -> None:
    """Проверяет write_log с именем файла из пробелов."""
    test_message = "Тест с пробелами"
    write_log(test_message, "   ")
    output = capture_output()
    assert test_message in output


def test_write_log_with_different_messages(temp_file_path: str, different_messages: str) -> None:
    """Проверяет write_log с разными типами сообщений."""
    message = different_messages
    write_log(message, temp_file_path)
    with open(temp_file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    assert content == message


@pytest.mark.parametrize("filename, should_create_file", [("test.log", True), ("  ", False), (None, False)])
def test_write_log_filename_variations(
    temp_directory: str, filename: Optional[str], should_create_file: bool, capture_output: Callable[[], str]
) -> None:
    """Проверяет write_log с разными вариантами имен файлов."""
    test_message = "Тестовое сообщение"
    full_path: Optional[str]
    if filename and filename.strip():
        full_path = os.path.join(temp_directory, filename.strip())
    elif filename == "  ":
        full_path = filename
    else:
        full_path = filename
    write_log(test_message, full_path)
    if should_create_file and full_path is not None:
        assert os.path.exists(full_path)
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        assert content == test_message
    else:
        output = capture_output()
        assert test_message in output


def test_log_decorator_basic(
    add_function: Callable[[int, int], int], temp_log_file: str, set_log_env_var: Callable[[str], None]
) -> None:
    """Проверяет базовую работу декоратора log."""
    set_log_env_var(temp_log_file)
    decorated_add = log()(add_function)  # Исправлено: добавлены ()
    result = decorated_add(3, 5)
    assert result == 8
    assert os.path.exists(temp_log_file)
    with open(temp_log_file, "r", encoding="utf-8") as f:
        log_content = f.read()
    assert "add" in log_content


def test_log_decorator_with_explicit_filename(
    multiply_function: Callable[[int, int], int], temp_log_file: str
) -> None:
    """Проверяет декоратор log с явным указанием имени файла."""
    decorated_multiply = log(filename=temp_log_file)(multiply_function)
    result = decorated_multiply(6, 7)
    assert result == 42
    with open(temp_log_file, "r", encoding="utf-8") as f:
        log_content = f.read()
    assert "multiply" in log_content.lower()


def test_log_decorator_preserves_name(add_function: Callable[[int, int], int]) -> None:
    """Проверяет, что декоратор сохраняет имя функции."""
    decorated_add = log()(add_function)  # Исправлено: добавлены ()
    assert decorated_add.__name__ == "add"


def test_log_decorator_different_syntax() -> None:
    """Проверяет синтаксис использования декоратора: @log() и @log(filename=...)."""

    @log()
    def func1() -> str:
        return "test1"

    @log()
    def func2() -> str:
        return "test2"

    assert func1() == "test1"
    assert func2() == "test2"


def test_log_decorator_with_error(
    divide_function: Callable[[int, int], float], temp_log_file: str, set_log_env_var: Callable[[str], None]
) -> None:
    """Проверяет, что декоратор правильно логирует ошибки."""
    set_log_env_var(temp_log_file)
    decorated_divide = log()(divide_function)  # Исправлено: добавлены ()
    with pytest.raises(ZeroDivisionError):
        decorated_divide(10, 0)
    assert os.path.exists(temp_log_file)
    with open(temp_log_file, "r", encoding="utf-8") as f:
        log_content = f.read()
    assert "ошибка" in log_content.lower() or "error" in log_content.lower()


def test_log_decorator_exception_propagation(function_that_fails: Callable[[], None], temp_log_file: str) -> None:
    """Проверяет, что декоратор пробрасывает исключения наружу."""
    decorated_fail = log(filename=temp_log_file)(function_that_fails)
    with pytest.raises(ValueError, match="Тестовая ошибка"):
        decorated_fail()
    assert os.path.exists(temp_log_file)


def test_log_decorator_with_class_method(temp_log_file: str) -> None:
    """Проверяет декоратор log на методах класса."""

    class DecoratedCalculator(Calculator):
        @log(filename=temp_log_file)
        def add(self, a: int, b: int) -> int:
            return super().add(a, b)

    calc = DecoratedCalculator()
    result = calc.add(10, 20)
    assert result == 30
    with open(temp_log_file, "r", encoding="utf-8") as f:
        log_content = f.read()
    assert "add" in log_content


def test_log_decorator_multiple_calls(counter_function: Callable[[], int], temp_log_file: str) -> None:
    """Проверяет декоратор при многократных вызовах функции."""
    decorated_counter = log(filename=temp_log_file)(counter_function)
    results = []
    for _ in range(3):
        results.append(decorated_counter())
    assert results == [1, 2, 3]
    with open(temp_log_file, "r", encoding="utf-8") as f:
        lines = [line for line in f if line.strip()]
    assert len(lines) >= 3


def test_log_decorator_with_args_kwargs(temp_log_file: str) -> None:
    """Проверяет декоратор на функции с *args и **kwargs."""

    def flexible_func(*args: Any, **kwargs: Any) -> int:
        return len(args) + len(kwargs)

    decorated_func = log(filename=temp_log_file)(flexible_func)
    result = decorated_func(1, 2, 3, name="Вася", age=25)
    assert result == 5
    with open(temp_log_file, "r", encoding="utf-8") as f:
        log_content = f.read()
    assert "1,2,3" in log_content or "name" in log_content


def test_log_decorator_env_variable(
    set_log_env_var: Callable[[str], None],
    clear_log_env_var: Callable[[], None],
    temp_log_file: str,
    capture_output: Callable[[], str],
) -> None:
    """Проверяет влияние переменной окружения LOG_FILE_PATH."""
    clear_log_env_var()

    @log()
    def test_func() -> str:
        return "test"

    result = test_func()
    assert result == "test"
    output = capture_output()
    assert "test_func" in output

    set_log_env_var(temp_log_file)

    result2 = test_func()
    assert result2 == "test"
    assert os.path.exists(temp_log_file)
    with open(temp_log_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "test_func" in content


@pytest.mark.slow
def test_log_decorator_recursive(temp_log_file: str) -> None:
    """Проверяет декоратор на рекурсивной функции."""
    global _factorial
    original_factorial = _factorial
    try:
        decorated = log(filename=temp_log_file)(_factorial)
        _factorial = decorated
        result = decorated(5)
        assert result == 120
        with open(temp_log_file, "r", encoding="utf-8") as f:
            lines = [line for line in f if line.strip()]
        assert len(lines) > 1
    finally:
        _factorial = original_factorial


def test_create_decorated_function(
    create_decorated_function: Callable[..., Callable[..., Any]], temp_log_file: str
) -> None:
    """Использует фикстуру для создания декорированной функции."""
    func = create_decorated_function(lambda x, y: x**y, filename=temp_log_file)
    result = func(2, 3)
    assert result == 8
    assert os.path.exists(temp_log_file)
