import pytest

from src.widget import get_date, mask_account_card


class TestMaskAccountCard:
    """Тесты для маскировки карт и счетов"""

    def test_valid_card_strings_from_fixture(self, valid_card_string_pair):
        """Тест валидных строк карт из фикстуры"""
        input_string, expected = valid_card_string_pair
        result = mask_account_card(input_string)
        assert result == expected

    def test_valid_account_strings_from_fixture(self, valid_account_string_pair):
        """Тест валидных строк счетов из фикстуры"""
        input_string, expected = valid_account_string_pair
        result = mask_account_card(input_string)
        assert result == expected

    def test_invalid_strings_from_fixture(self, invalid_string_pair):
        """Тест невалидных строк из фикстуры"""
        input_string, expected = invalid_string_pair
        result = mask_account_card(input_string)
        assert result == expected

    def test_formatted_strings_from_fixture(self, formatted_string_pair):
        """Тест отформатированных строк из фикстуры"""
        input_string, expected = formatted_string_pair
        result = mask_account_card(input_string)
        assert result == expected

    @pytest.mark.parametrize(
        "input_string, expected",
        [
            ("Visa Gold 1111222233334444", "Visa Gold 1111 22** **** 4444"),
            ("Maestro Debit 5555666677778888", "Maestro Debit 5555 66** **** 8888"),
        ],
    )
    def test_additional_card_strings_parametrized(self, input_string, expected):
        """Дополнительные параметризованные тесты строк карт"""
        result = mask_account_card(input_string)
        assert result == expected

    @pytest.mark.parametrize(
        "input_string, expected",
        [
            ("Счет 11112222333344445555", "Счет **5555"),
            ("Счет 99998888777766665544", "Счет **5544"),
        ],
    )
    def test_additional_account_strings_parametrized(self, input_string, expected):
        """Дополнительные параметризованные тесты строк счетов"""
        result = mask_account_card(input_string)
        assert result == expected


    def test_card_with_invalid_number(self):
        """Тест карты с некорректным номером"""
        result = mask_account_card("Visa 123")
        assert result == ""

    def test_account_with_invalid_number(self):
        """Тест счета с некорректным номером"""
        result = mask_account_card("Счет 123")
        assert result == ""

    @pytest.mark.parametrize(
        "input_string, expected",
        [
            ("счет 73654108430135874305", ""),
            ("СЧЕТ 73654108430135874305", ""),
            ("VISA 7000792289606361", ""),
        ],
    )
    def test_case_sensitive_strings_parametrized(self, input_string, expected):
        """Параметризованный тест чувствительности к регистру"""
        result = mask_account_card(input_string)
        assert result == expected


class TestGetDate:
    """Тесты для форматирования даты"""

    def test_valid_dates_from_fixture(self, valid_date_pair):
        """Тест валидных дат из фикстуры"""
        date_string, expected = valid_date_pair
        result = get_date(date_string)
        assert result == expected

    def test_invalid_dates_from_fixture(self, invalid_date_pair):
        """Тест невалидных дат из фикстуры"""
        date_string, expected = invalid_date_pair
        result = get_date(date_string)
        assert result == expected

    def test_dates_with_timezone_from_fixture(self, date_with_timezone_pair):
        """Тест дат с часовым поясом из фикстуры"""
        date_string, expected = date_with_timezone_pair
        result = get_date(date_string)
        assert result == expected

    def test_dates_with_milliseconds_from_fixture(self, date_with_milliseconds_pair):
        """Тест дат с миллисекундами из фикстуры"""
        date_string, expected = date_with_milliseconds_pair
        result = get_date(date_string)
        assert result == expected

    @pytest.mark.parametrize(
        "date_string, expected",
        [
            ("2023-02-28", "28.02.2023"),
            ("2023-03-31", "31.03.2023"),
            ("2023-04-30", "30.04.2023"),
            ("2023-05-31", "31.05.2023"),
        ],
    )
    def test_month_boundaries_parametrized(self, date_string, expected):
        """Параметризованный тест граничных значений месяцев"""
        result = get_date(date_string)
        assert result == expected


    @pytest.mark.parametrize(
        "date_string, expected",
        [
            ("  2023-01-15  ", ""),
            ("2023-01-15  ", ""),
            ("  2023-01-15", ""),
        ],
    )
    def test_dates_with_whitespace_parametrized(self, date_string, expected):
        """Параметризованный тест дат с пробелами"""
        result = get_date(date_string)
        assert result == expected

    @pytest.mark.parametrize(
        "date_string, expected",
        [
            ("2024-02-29", "29.02.2024"),
            ("2023-02-29", ""),
            ("2000-02-29", "29.02.2000"),
        ],
    )
    def test_leap_years_parametrized(self, date_string, expected):
        """Параметризованный тест високосных годов"""
        result = get_date(date_string)
        assert result == expected
