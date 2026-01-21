import pytest
from src.masks import get_mask_card_number, get_mask_account


class TestGetMaskCardNumber:
    """Тесты для маскировки номера карты"""

    def test_valid_card_numbers_from_fixture(self, valid_card_number_pair):
        """Тест валидных номеров карт из фикстуры"""
        card_number, expected = valid_card_number_pair
        result = get_mask_card_number(card_number)
        assert result == expected

    def test_formatted_card_numbers_from_fixture(self, formatted_card_number_pair):
        """Тест отформатированных номеров карт из фикстуры"""
        card_number, expected = formatted_card_number_pair
        result = get_mask_card_number(card_number)
        assert result == expected

    def test_invalid_card_numbers_from_fixture(self, invalid_card_number):
        """Тест невалидных номеров карт из фикстуры"""
        card_number, description = invalid_card_number
        with pytest.raises(ValueError) as exc_info:
            get_mask_card_number(card_number)
        assert "16 цифр" in str(exc_info.value)

    @pytest.mark.parametrize("card_number, expected", [
        ("1111222233334444", "1111 22** **** 4444"),
        ("5555666677778888", "5555 66** **** 8888"),
    ])
    def test_additional_valid_card_numbers_parametrized(self, card_number, expected):
        """Дополнительные параметризованные тесты валидных номеров карт"""
        result = get_mask_card_number(card_number)
        assert result == expected

    @pytest.mark.parametrize("card_number, error_message", [
        ("", "Номер карты должен содержать 16 цифр, получено 0"),
        ("123", "Номер карты должен содержать 16 цифр, получено 3"),
    ])
    def test_additional_invalid_card_numbers_parametrized(self, card_number, error_message):
        """Дополнительные параметризованные тесты невалидных номеров карт"""
        with pytest.raises(ValueError, match=error_message):
            get_mask_card_number(card_number)

    def test_card_number_whitespace_only(self):
        """Тест с номером карты, содержащим только пробелы"""
        with pytest.raises(ValueError) as exc_info:
            get_mask_card_number("   ")
        assert "16 цифр" in str(exc_info.value)


class TestGetMaskAccount:
    """Тесты для маскировки номера счета"""

    def test_valid_account_numbers_from_fixture(self, valid_account_number_pair):
        """Тест валидных номеров счетов из фикстуры"""
        account_number, expected = valid_account_number_pair
        result = get_mask_account(account_number)
        assert result == expected

    def test_formatted_account_numbers_from_fixture(self, formatted_account_number_pair):
        """Тест отформатированных номеров счетов из фикстуры"""
        account_number, expected = formatted_account_number_pair
        result = get_mask_account(account_number)
        assert result == expected

    def test_invalid_account_numbers_from_fixture(self, invalid_account_number):
        """Тест невалидных номеров счетов из фикстуры"""
        account_number, description = invalid_account_number
        with pytest.raises(ValueError) as exc_info:
            get_mask_account(account_number)
        assert "минимум 4 цифры" in str(exc_info.value)

    @pytest.mark.parametrize("account_number, expected", [
        ("11112222333344445555", "**5555"),
        ("99998888777766665544", "**5544"),
    ])
    def test_additional_valid_account_numbers_parametrized(self, account_number, expected):
        """Дополнительные параметризованные тесты валидных номеров счетов"""
        result = get_mask_account(account_number)
        assert result == expected

    @pytest.mark.parametrize("account_number, error_message", [
        ("", "Номер счета должен содержать минимум 4 цифры, получено 0"),
        ("12", "Номер счета должен содержать минимум 4 цифры, получено 2"),
    ])
    def test_additional_invalid_account_numbers_parametrized(self, account_number, error_message):
        """Дополнительные параметризованные тесты невалидных номеров счетов"""
        with pytest.raises(ValueError, match=error_message):
            get_mask_account(account_number)

    def test_long_account_number(self):
        """Тест очень длинного номера счета"""
        long_account = "1" * 50 + "1234"
        result = get_mask_account(long_account)
        assert result == "**1234"

    def test_account_with_only_last_four(self):
        """Тест счета, где последние 4 цифры - это весь номер"""
        result = get_mask_account("1234")
        assert result == "**1234"