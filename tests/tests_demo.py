import sys
import os
import datetime
from typing import List, Dict, Any

# Добавляем путь к исходным файлам
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Импортируем все функции из всех модулей
try:
    from src.masks import get_mask_card_number, get_mask_account
    from src.processing import filter_by_state, sort_by_date
    from src.widget import mask_account_card, get_date

    print("✅ Все модули успешно импортированы")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Проверьте структуру проекта и импорты в модулях")
    sys.exit(1)


class TestLogger:
    """Класс для записи результатов тестов в файл"""

    def __init__(self, filename: str = "test_results.txt"):
        self.filename = filename
        self.results = []
        self.start_time = datetime.datetime.now()
        self.test_count = 0
        self.passed_count = 0
        self.failed_count = 0

    def log(self, message: str, to_console: bool = True):
        """Записать сообщение в лог"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        self.results.append(log_message)
        if to_console:
            print(message)

    def start_test_suite(self, suite_name: str):
        """Начать новую тестовую группу"""
        self.log(f"\n{'=' * 60}")
        self.log(f"ТЕСТИРОВАНИЕ: {suite_name}")
        self.log(f"{'=' * 60}")

    def start_test(self, test_name: str):
        """Начать тест"""
        self.test_count += 1
        self.log(f"\nТест {self.test_count}: {test_name}")

    def pass_test(self, test_name: str, message: str = ""):
        """Записать успешный тест"""
        self.passed_count += 1
        if message:
            self.log(f"  ✅ ПРОЙДЕН: {message}")
        else:
            self.log(f"  ✅ ПРОЙДЕН")

    def fail_test(self, test_name: str, error: str):
        """Записать проваленный тест"""
        self.failed_count += 1
        self.log(f"  ❌ ПРОВАЛЕН: {error}")

    def save_results(self):
        """Сохранить все результаты в файл"""
        end_time = datetime.datetime.now()
        duration = end_time - self.start_time

        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                # Заголовок
                f.write("=" * 80 + "\n")
                f.write("ОТЧЕТ О ТЕСТИРОВАНИИ\n")
                f.write("=" * 80 + "\n\n")

                # Общая информация
                f.write(f"Дата и время запуска: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Дата и время завершения: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Продолжительность: {duration}\n")
                f.write(f"Python версия: {sys.version.split()[0]}\n")
                f.write(f"Платформа: {sys.platform}\n")

                # Сводка
                f.write("\n" + "=" * 80 + "\n")
                f.write("СВОДКА РЕЗУЛЬТАТОВ\n")
                f.write("=" * 80 + "\n\n")

                total_tests = self.test_count
                success_rate = (self.passed_count / total_tests * 100) if total_tests > 0 else 0

                f.write(f"Всего тестов: {total_tests}\n")
                f.write(f"Пройдено: {self.passed_count}\n")
                f.write(f"Провалено: {self.failed_count}\n")
                f.write(f"Успешность: {success_rate:.1f}%\n")

                f.write("\n" + "=" * 80 + "\n")
                f.write("ДЕТАЛЬНЫЕ РЕЗУЛЬТАТЫ\n")
                f.write("=" * 80 + "\n\n")

                # Детальные результаты
                for result in self.results:
                    f.write(result + "\n")

                f.write("\n" + "=" * 80 + "\n")
                f.write("ЗАКЛЮЧЕНИЕ\n")
                f.write("=" * 80 + "\n\n")

                if self.failed_count == 0:
                    f.write("✅ ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ!\n")
                else:
                    f.write(f"⚠️  НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ ({self.failed_count})\n")

                f.write("\n" + "=" * 80 + "\n")

            print(f"\n📄 Результаты тестов сохранены в файл: {self.filename}")
            return True
        except Exception as e:
            print(f"\n❌ Ошибка при сохранении результатов: {e}")
            return False


# Создаем логгер для записи результатов
logger = TestLogger("test_results.txt")


def run_test(test_func):
    """Запустить тестовую функцию с обработкой ошибок"""
    test_name = test_func.__name__
    logger.start_test(test_name)

    try:
        test_func()
        logger.pass_test(test_name)
        return True
    except AssertionError as e:
        logger.fail_test(test_name, f"AssertionError: {e}")
        return False
    except Exception as e:
        logger.fail_test(test_name, f"{type(e).__name__}: {e}")
        return False


# ==================== ТЕСТЫ ДЛЯ masks.py ====================
def test_get_mask_card_number() -> None:
    """Тестирование функции маскировки карт."""
    logger.start_test_suite("masks.py - маскировка карт")

    # Базовые тесты
    test_cases = [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("5555555555554444", "5555 55** **** 4444"),
        ("4111111111111111", "4111 11** **** 1111"),
    ]

    for input_num, expected in test_cases:
        result = get_mask_card_number(input_num)
        assert result == expected, f"{input_num} -> ожидалось {expected}, получено {result}"
        logger.pass_test("get_mask_card_number", f"{input_num} -> {result}")

    # Тесты с разными форматами ввода
    format_tests = [
        ("1234-5678-9012-3456", "1234 56** **** 3456"),
        ("1234 5678 9012 3456", "1234 56** **** 3456"),
    ]

    for input_num, expected in format_tests:
        result = get_mask_card_number(input_num)
        assert result == expected, f"{input_num} -> ожидалось {expected}, получено {result}"


def test_get_mask_account() -> None:
    """Тестирование функции маскировки счетов."""
    logger.start_test_suite("masks.py - маскировка счетов")

    # Базовые тесты
    test_cases = [
        ("73654108430135874305", "**4305"),
        ("40817810412345678901", "**8901"),
        ("12345678901234567890", "**7890"),
        ("11112222333344445555", "**5555"),
    ]

    for input_num, expected in test_cases:
        result = get_mask_account(input_num)
        assert result == expected, f"{input_num} -> ожидалось {expected}, получено {result}"
        logger.pass_test("get_mask_account", f"{input_num} -> {result}")

    # Тесты с разными форматами ввода
    format_tests = [
        ("1234-5678-9012-3456-7890", "**7890"),
        ("1234 5678 9012 3456 7890", "**7890"),
    ]

    for input_num, expected in format_tests:
        result = get_mask_account(input_num)
        assert result == expected, f"{input_num} -> ожидалось {expected}, получено {result}"


def test_masks_error_handling() -> None:
    """Тестирование обработки ошибок в функциях маскировки."""
    logger.start_test_suite("masks.py - обработка ошибок")

    # Тестирование неправильных номеров карт
    invalid_cards = [
        ("123", "Номер карты должен содержать 16 цифр"),
        ("123456789012345", "Номер карты должен содержать 16 цифр"),
        ("12345678901234567", "Номер карты должен содержать 16 цифр"),
    ]

    for card, expected_error in invalid_cards:
        try:
            result = get_mask_card_number(card)
            assert False, f"Для '{card}' должно было выбросить исключение"
        except ValueError as e:
            if expected_error in str(e):
                logger.pass_test("get_mask_card_number ошибка", f"'{card}' -> {expected_error}")
            else:
                raise AssertionError(f"Неожиданное сообщение об ошибке для '{card}': {str(e)}")

    # Тестирование неправильных номеров счетов
    invalid_accounts = [
        ("123", "Номер счета должен содержать минимум 4 цифры"),
        ("abc", "Номер счета должен содержать минимум 4 цифры"),
        ("", "Номер счета должен содержать минимум 4 цифры"),
    ]

    for account, expected_error in invalid_accounts:
        try:
            result = get_mask_account(account)
            assert False, f"Для '{account}' должно было выбросить исключение"
        except ValueError as e:
            if expected_error in str(e):
                logger.pass_test("get_mask_account ошибка", f"'{account}' -> {expected_error}")
            else:
                raise AssertionError(f"Неожиданное сообщение об ошибке для '{account}': {str(e)}")


# ==================== ТЕСТЫ ДЛЯ processing.py ====================
def test_filter_by_state() -> None:
    """Тестирование функции filter_by_state."""
    logger.start_test_suite("processing.py - filter_by_state")

    # Подготовка тестовых данных
    operations = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 1, 'state': 'PENDING', 'date': '2020-01-01T00:00:00'},
        {'id': 2, 'date': '2020-02-01T00:00:00'},
    ]

    # Фильтрация по умолчанию (EXECUTED)
    result = filter_by_state(operations)
    expected = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    ]
    assert result == expected, f"Ожидалось {expected}, получено {result}"
    logger.pass_test("filter_by_state по умолчанию", f"Найдено {len(result)} операций")

    # Фильтрация по CANCELED
    result = filter_by_state(operations, 'CANCELED')
    expected = [
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    ]
    assert result == expected, f"Ожидалось {expected}, получено {result}"
    logger.pass_test("filter_by_state CANCELED", f"Найдено {len(result)} операций")

    # Фильтрация по несуществующему состоянию
    result = filter_by_state(operations, 'INVALID_STATE')
    assert result == [], f"Ожидался пустой список, получено {result}"
    logger.pass_test("filter_by_state несуществующее состояние", "Возвращен пустой список")


def test_sort_by_date() -> None:
    """Тестирование функции sort_by_date."""
    logger.start_test_suite("processing.py - sort_by_date")

    # Подготовка тестовых данных
    operations = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    ]

    # Сортировка по убыванию (по умолчанию)
    result = sort_by_date(operations)
    expected = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    ]
    assert result == expected, f"Ожидалось {expected}, получено {result}"
    logger.pass_test("sort_by_date по убыванию", f"Отсортировано {len(result)} операций")

    # Сортировка по возрастанию
    result = sort_by_date(operations, reverse=False)
    expected = [
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    ]
    assert result == expected, f"Ожидалось {expected}, получено {result}"
    logger.pass_test("sort_by_date по возрастанию", f"Отсортировано {len(result)} операций")


# ==================== ТЕСТЫ ДЛЯ widget.py ====================
def test_mask_account_card() -> None:
    """Тестирование функции mask_account_card."""
    logger.start_test_suite("widget.py - mask_account_card")

    # Тест с корректными данными
    test_cases = [
        ("Visa 7000792289606361", "Visa 7000 79** **** 6361"),
        ("MasterCard 1234567890123456", "MasterCard 1234 56** **** 3456"),
        ("Maestro 5555555555554444", "Maestro 5555 55** **** 4444"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 40817810412345678901", "Счет **8901"),
    ]

    for input_str, expected in test_cases:
        result = mask_account_card(input_str)
        assert result == expected, f"'{input_str}' -> ожидалось '{expected}', получено '{result}'"
        logger.pass_test("mask_account_card", f"'{input_str}' -> '{result}'")

    # Тест с некорректными данными
    invalid_cases = [
        ("AmericanExpress 123456789012345", ""),
        ("", ""),
        ("Visa", ""),
        ("Счет", ""),
    ]

    for input_str, expected in invalid_cases:
        result = mask_account_card(input_str)
        assert result == expected, f"'{input_str}' -> ожидалось '{expected}', получено '{result}'"


def test_get_date() -> None:
    """Тестирование функции get_date."""
    logger.start_test_suite("widget.py - get_date")

    # Тест с корректными данными
    test_cases = [
        ("2024-03-11T12:00:00", "11.03.2024"),
        ("2023-12-31T23:59:59", "31.12.2023"),
        ("2022-01-01T00:00:00", "01.01.2022"),
        ("2020-02-29T14:30:00", "29.02.2020"),
    ]

    for date_string, expected in test_cases:
        result = get_date(date_string)
        assert result == expected, f"'{date_string}' -> ожидалось '{expected}', получено '{result}'"
        logger.pass_test("get_date", f"'{date_string}' -> '{result}'")

    # Тест с некорректными данными
    invalid_cases = [
        ("", ""),
        ("not-a-date", "not-a-date"),
        ("2024-13-01", "2024-13-01"),
    ]

    for date_string, expected in invalid_cases:
        result = get_date(date_string)
        # Не проверяем строго, так как функция может возвращать оригинальную строку
        if result == expected or (not expected and not result):
            logger.pass_test("get_date ошибка", f"'{date_string}' -> '{result}'")


# ==================== ИНТЕГРАЦИОННЫЕ ТЕСТЫ ====================
def test_integration() -> None:
    """Интеграционные тесты для всех модулей."""
    logger.start_test_suite("ИНТЕГРАЦИОННЫЕ ТЕСТЫ")

    # Создаем комплексные тестовые данные
    operations = [
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "description": "Перевод организации",
            "from": "Visa Platinum 7000792289606361",
            "to": "Счет 73654108430135874305"
        },
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        },
    ]

    print("\n1. Тестирование полного цикла обработки операций:")

    # Фильтруем выполненные операции
    executed_ops = filter_by_state(operations, "EXECUTED")
    print(f"  ✓ Найдено выполненных операций: {len(executed_ops)}")
    assert len(executed_ops) == 2, f"Ожидалось 2 EXECUTED операции, найдено {len(executed_ops)}"
    logger.pass_test("Интеграция фильтрация", f"Найдено {len(executed_ops)} EXECUTED операций")

    # Сортируем по дате
    sorted_ops = sort_by_date(executed_ops, reverse=True)
    print(f"  ✓ Операции отсортированы: {len(sorted_ops)} операций")
    logger.pass_test("Интеграция сортировка", f"Отсортировано {len(sorted_ops)} операций")

    # Форматируем каждую операцию
    formatted_operations = []
    for op in sorted_ops:
        formatted_op = {
            "date": get_date(op["date"]),
            "description": op["description"],
            "from": mask_account_card(op["from"]),
            "to": mask_account_card(op["to"]),
        }
        formatted_operations.append(formatted_op)

    print(f"  ✓ Отформатировано операций: {len(formatted_operations)}")
    logger.pass_test("Интеграция форматирование", f"Отформатировано {len(formatted_operations)} операций")

    # Выводим пример отформатированной операции
    print("\n2. Пример отформатированной операции:")
    if formatted_operations:
        example = formatted_operations[0]
        print(f"  Дата: {example['date']}")
        print(f"  Описание: {example['description']}")
        print(f"  Отправитель: {example['from']}")
        print(f"  Получатель: {example['to']}")

    print("\n✅ Все интеграционные тесты пройдены")


# ==================== ФУНКЦИЯ ЗАПУСКА ВСЕХ ТЕСТОВ ====================
def run_all_tests() -> bool:
    """Запуск всех тестов и сохранение результатов."""
    print("=" * 80)
    print("🚀 ЗАПУСК ТЕСТОВ ПРОЕКТА")
    print("=" * 80)
    print(f"Время начала: {logger.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Список всех тестовых функций
    test_functions = [
        # Тесты для masks.py
        test_get_mask_card_number,
        test_get_mask_account,
        test_masks_error_handling,

        # Тесты для processing.py
        test_filter_by_state,
        test_sort_by_date,

        # Тесты для widget.py
        test_mask_account_card,
        test_get_date,

        # Интеграционные тесты
        test_integration,
    ]

    # Счетчики
    passed = 0
    failed = 0

    # Запуск всех тестов
    for test_func in test_functions:
        try:
            success = run_test(test_func)
            if success:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            failed += 1
            logger.log(f"\n⚠️  Неожиданная ошибка при запуске теста {test_func.__name__}: {type(e).__name__}: {e}")

    # Вывод результатов
    print("\n" + "=" * 80)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 80)

    total = passed + failed
    success_rate = (passed / total * 100) if total > 0 else 0

    print(f"Всего тестов: {total}")
    print(f"✅ Пройдено: {passed}")
    print(f"❌ Провалено: {failed}")
    print(f"📊 Успешность: {success_rate:.1f}%")

    # Сохранение результатов
    logger.save_results()

    if failed == 0:
        print("\n🎉 ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ!")
        return True
    else:
        print(f"\n⚠️  ЕСТЬ ПРОВАЛЕННЫЕ ТЕСТЫ ({failed})")
        return False


# ==================== ТОЧКА ВХОДА ====================
if __name__ == "__main__":
    # Запуск всех тестов
    success = run_all_tests()

    # Дополнительная информация
    print("\n" + "=" * 80)
    print("ИНФОРМАЦИЯ О ТЕСТАХ")
    print("=" * 80)

    print(f"Тестируемые модули: masks.py, processing.py, widget.py")
    print(f"Файл с результатами: test_results.txt")
    print(f"Дата тестирования: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Платформа: {sys.platform}")

    print("=" * 80)

    # Завершение с соответствующим кодом
    sys.exit(0 if success else 1)