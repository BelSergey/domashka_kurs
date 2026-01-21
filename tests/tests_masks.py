import pytest
from src.masks import get_mask_card_number, get_mask_account


class TestGetMaskCardNumber:
    """Тесты для маскировки номера карты"""

    @pytest.fixture
    def valid_card_numbers(self):
        """Фикстура с валидными номерами карт"""
        return [
            ("7000792289606361", "7000 79** **** 6361"),
            ("1596837868705199", "1596 83** **** 5199"),
            ("7158300734726758", "7158 30** **** 6758"),
            ("1234567812345678", "1234 56** **** 5678"),
            ("0000000000000000", "0000 00** **** 0000"),
            ("9999999999999999", "9999 99** **** 9999"),
        ]

    @pytest.fixture
    def invalid_card_numbers(self):
        """Фикстура с невалидными номерами карт"""
        return [
            ("123456789012345", "15 цифр"),
            ("12345678901234567", "17 цифр"),
            ("", "пустая строка"),
            ("abcd-efgh-ijkl-mnop", "не цифры"),
            ("7000 7922", "слишком короткий"),
        ]

    @pytest.fixture
    def formatted_card_numbers(self):
        """Фикстура с отформатированными номерами карт"""
        return [
            ("7000 7922 8960 6361", "7000 79** **** 6361"),
            ("7000-7922-8960-6361", "7000 79** **** 6361"),
            ("7000 7922-8960 6361", "7000 79** **** 6361"),
            ("7000.7922.8960.6361", "7000 79** **** 6361"),
        ]

    @pytest.mark.parametrize("card_number, expected", [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1596837868705199", "1596 83** **** 5199"),
        ("7158300734726758", "7158 30** **** 6758"),
        ("0000000000000000", "0000 00** **** 0000"),
        ("9999999999999999", "9999 99** **** 9999"),
    ])
    def test_valid_card_numbers_parametrized(self, card_number, expected):
        """Параметризованный тест валидных номеров карт"""
        result = get_mask_card_number(card_number)
        assert result == expected

    def test_valid_card_numbers_fixture(self, valid_card_numbers):
        """Тест валидных номеров карт из фикстуры"""
        for card_number, expected in valid_card_numbers:
            result = get_mask_card_number(card_number)
            assert result == expected

    def test_formatted_card_numbers(self, formatted_card_numbers):
        """Тест отформатированных номеров карт"""
        for card_number, expected in formatted_card_numbers:
            result = get_mask_card_number(card_number)
            assert result == expected

    @pytest.mark.parametrize("card_number, description", [
        ("123456789012345", "15 цифр"),
        ("12345678901234567", "17 цифр"),
        ("", "пустая строка"),
        ("abcd-efgh-ijkl-mnop", "не цифры"),
        ("7000 7922", "слишком короткий"),
    ])
    def test_invalid_card_numbers_parametrized(self, card_number, description):
        """Параметризованный тест невалидных номеров карт"""
        with pytest.raises(ValueError) as exc_info:
            get_mask_card_number(card_number)
        assert "16 цифр" in str(exc_info.value)

    def test_card_number_whitespace_only(self):
        """Тест с номером карты, содержащим только пробелы"""
        with pytest.raises(ValueError) as exc_info:
            get_mask_card_number("   ")
        assert "16 цифр" in str(exc_info.value)


class TestGetMaskAccount:
    """Тесты для маскировки номера счета"""

    @pytest.fixture
    def valid_account_numbers(self):
        """Фикстура с валидными номерами счетов"""
        return [
            ("73654108430135874305", "**4305"),
            ("35383033474447895560", "**5560"),
            ("1234", "**1234"),
            ("9876543210", "**3210"),
            ("00000000000000000000", "**0000"),
            ("99999999999999999999", "**9999"),
        ]

    @pytest.fixture
    def invalid_account_numbers(self):
        """Фикстура с невалидными номерами счетов"""
        return [
            ("123", "3 цифры"),
            ("12", "2 цифры"),
            ("1", "1 цифра"),
            ("", "пустая строка"),
            ("abc", "не цифры"),
        ]

    @pytest.fixture
    def formatted_account_numbers(self):
        """Фикстура с отформатированными номерами счетов"""
        return [
            ("7365 4108 4301 3587 4305", "**4305"),
            ("7365-4108-4301-3587-4305", "**4305"),
            ("7365.4108.4301.3587.4305", "**4305"),
            ("7365 4108-4301 3587.4305", "**4305"),
        ]

    @pytest.mark.parametrize("account_number, expected", [
        ("73654108430135874305", "**4305"),
        ("35383033474447895560", "**5560"),
        ("1234", "**1234"),
        ("9876543210", "**3210"),
        ("00000000000000000000", "**0000"),
    ])
    def test_valid_account_numbers_parametrized(self, account_number, expected):
        """Параметризованный тест валидных номеров счетов"""
        result = get_mask_account(account_number)
        assert result == expected

    def test_valid_account_numbers_fixture(self, valid_account_numbers):
        """Тест валидных номеров счетов из фикстуры"""
        for account_number, expected in valid_account_numbers:
            result = get_mask_account(account_number)
            assert result == expected

    def test_formatted_account_numbers(self, formatted_account_numbers):
        """Тест отформатированных номеров счетов"""
        for account_number, expected in formatted_account_numbers:
            result = get_mask_account(account_number)
            assert result == expected

    @pytest.mark.parametrize("account_number, description", [
        ("123", "3 цифры"),
        ("12", "2 цифры"),
        ("", "пустая строка"),
        ("abc", "не цифры"),
        ("   ", "пробелы"),
    ])
    def test_invalid_account_numbers_parametrized(self, account_number, description):
        """Параметризованный тест невалидных номеров счетов"""
        with pytest.raises(ValueError) as exc_info:
            get_mask_account(account_number)
        assert "минимум 4 цифры" in str(exc_info.value)

    def test_long_account_number(self):
        """Тест очень длинного номера счета"""
        long_account = "1" * 50 + "1234"
        result = get_mask_account(long_account)
        assert result == "**1234"

    def test_account_with_only_last_four(self):
        """Тест счета, где последние 4 цифры - это весь номер"""
        result = get_mask_account("1234")
        assert result == "**1234"