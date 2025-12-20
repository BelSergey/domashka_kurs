
import sys
import os


sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.masks import get_mask_card_number, get_mask_account


def test_card_masking() -> None:
    """Тестирование маскировки карт."""
    test_cases = [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("5555555555554444", "5555 55** **** 4444"),
        ("4111111111111111", "4111 11** **** 1111"),
    ]

    print("Тестирование маскировки карт:")
    for input_num, expected in test_cases:
        result = get_mask_card_number(input_num)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {input_num} -> {result}")
        assert result == expected, f"Ожидалось: {expected}, получено: {result}"

    print("Все тесты карт пройдены!\n")


def test_account_masking() -> None:
    """Тестирование маскировки счетов."""
    test_cases = [
        ("73654108430135874305", "**4305"),
        ("40817810412345678901", "**8901"),
        ("12345678901234567890", "**7890"),
        ("11112222333344445555", "**5555"),
    ]

    print("Тестирование маскировки счетов:")
    for input_num, expected in test_cases:
        result = get_mask_account(input_num)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {input_num} -> {result}")
        assert result == expected, f"Ожидалось: {expected}, получено: {result}"

    print("Все тесты счетов пройдены!\n")


def test_error_handling() -> None:
    """Тестирование обработки ошибок."""
    print("Тестирование обработки ошибок:")

    invalid_cards = [
        "123",
        "123456789012345",
        "12345678901234567",
        "abcdefghijklmnop",
    ]

    for card in invalid_cards:
        try:
            get_mask_card_number(card)
            print(f"  ✗ Не выброшено исключение для: {card}")
            assert False, f"Должно было выбросить ValueError для: {card}"
        except ValueError:
            print(f"  ✓ Корректно обработана ошибка для: {card}")

    # Тестирование неправильных номеров счетов
    invalid_accounts = [
        "123",  # Слишком короткий
        "abc",  # Не цифры
        "",  # Пустая строка
    ]

    for account in invalid_accounts:
        try:
            get_mask_account(account)
            print(f"  ✗ Не выброшено исключение для: '{account}'")
            assert False, f"Должно было выбросить ValueError для: '{account}'"
        except ValueError:
            print(f"  ✓ Корректно обработана ошибка для: '{account}'")

    print("Все тесты обработки ошибок пройдены!\n")


if __name__ == "__main__":
    print("=" * 50)
    print("Начало тестирования модуля masks")
    print("=" * 50)

    test_card_masking()
    test_account_masking()
    test_error_handling()

    print("=" * 50)
    print("Все тесты успешно пройдены!")
    print("=" * 50)