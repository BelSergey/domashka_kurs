import unittest
from unittest.mock import patch, MagicMock
from src.external_api import get_amount_in_rub


class TestGetAmountInRub(unittest.TestCase):
    """Тесты для функции get_amount_in_rub"""
    def test_rub_transaction_returns_same_amount(self):
        """Тест: транзакция уже в рублях возвращает ту же сумму"""
        transaction = {
            "id": 1,
            "operationAmount": {
                "amount": "1000.50",
                "currency": {
                    "code": "RUB",
                    "name": "рубль"
                }
            }
        }

        result = get_amount_in_rub(transaction)

        self.assertEqual(result, 1000.5)

    @patch('src.external_api.os.getenv')
    @patch('src.external_api.requests.get')
    def test_usd_transaction_converts_successfully(self, mock_requests_get, mock_getenv):
        """Тест: USD транзакция успешно конвертируется в RUB"""
        transaction = {
            "id": 2,
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "USD",
                    "name": "доллар США"
                }
            }
        }

        mock_getenv.return_value = "test_api_key_123"

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "success": True,
            "result": 7500.50
        }
        mock_requests_get.return_value = mock_response

        result = get_amount_in_rub(transaction)

        self.assertEqual(result, 7500.5)
        mock_getenv.assert_called_once_with("exchange_rates_data_api_key")
        mock_requests_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/convert",
            headers={"apikey": "test_api_key_123"},
            params={"from": "USD", "to": "RUB", "amount": 100.0},
            timeout=10
        )

    @patch('src.external_api.os.getenv')
    @patch('src.external_api.requests.get')
    def test_eur_transaction_converts_successfully(self, mock_requests_get, mock_getenv):
        """Тест: EUR транзакция успешно конвертируется в RUB"""
        transaction = {
            "id": 3,
            "operationAmount": {
                "amount": "50.00",
                "currency": {
                    "code": "EUR",
                    "name": "евро"
                }
            }
        }

        mock_getenv.return_value = "test_api_key"

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "success": True,
            "result": 4000.25
        }
        mock_requests_get.return_value = mock_response

        result = get_amount_in_rub(transaction)

        self.assertEqual(result, 4000.25)

    def test_unsupported_currency_returns_none(self):
        """Тест: неподдерживаемая валюта возвращает None"""
        # Arrange
        transaction = {
            "id": 4,
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "GBP",
                    "name": "фунт стерлингов"
                }
            }
        }

        # Act
        result = get_amount_in_rub(transaction)

        # Assert
        self.assertIsNone(result)

    # Тест 5: Отсутствие API ключа
    @patch('src.external_api.os.getenv')
    def test_no_api_key_returns_none(self, mock_getenv):
        """Тест: отсутствие API ключа возвращает None"""
        # Arrange
        transaction = {
            "id": 5,
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "USD",
                    "name": "доллар США"
                }
            }
        }

        mock_getenv.return_value = None

        # Act
        result = get_amount_in_rub(transaction)

        # Assert
        self.assertIsNone(result)
        mock_getenv.assert_called_once_with("exchange_rates_data_api_key")

    # Тест 6: API возвращает ошибку
    @patch('src.external_api.os.getenv')
    @patch('src.external_api.requests.get')
    def test_api_error_returns_none(self, mock_requests_get, mock_getenv):
        """Тест: ошибка API возвращает None"""
        # Arrange
        transaction = {
            "id": 6,
            "operationAmount": {
                "amount": "50.00",
                "currency": {
                    "code": "USD",
                    "name": "доллар США"
                }
            }
        }

        mock_getenv.return_value = "test_api_key"

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "success": False,
            "error": {"info": "Invalid API key"}
        }
        mock_requests_get.return_value = mock_response

        # Act
        result = get_amount_in_rub(transaction)

        # Assert
        self.assertIsNone(result)

    # Тест 7: Ошибка сети при запросе к API
    @patch('src.external_api.os.getenv')
    @patch('src.external_api.requests.get')
    def test_network_error_returns_none(self, mock_requests_get, mock_getenv):
        """Тест: ошибка сети возвращает None"""
        # Arrange
        transaction = {
            "id": 7,
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "USD",
                    "name": "доллар США"
                }
            }
        }

        mock_getenv.return_value = "test_api_key"
        mock_requests_get.side_effect = ConnectionError("Network error")

        # Act
        result = get_amount_in_rub(transaction)

        # Assert
        self.assertIsNone(result)

    # Тест 8: Транзакция без operationAmount
    def test_transaction_without_operation_amount_returns_none(self):
        """Тест: транзакция без operationAmount возвращает None"""
        # Arrange
        transaction = {
            "id": 8,
            "description": "Тестовая транзакция",
            "from": "Счет 1234567890",
            "to": "Счет 0987654321"
        }

        # Act
        result = get_amount_in_rub(transaction)

        # Assert
        self.assertIsNone(result)

    # Тест 9: Неверный формат суммы
    def test_invalid_amount_format_returns_none(self):
        """Тест: неверный формат суммы возвращает None"""
        # Arrange
        transaction = {
            "id": 9,
            "operationAmount": {
                "amount": "не число",
                "currency": {
                    "code": "RUB",
                    "name": "рубль"
                }
            }
        }

        # Act
        result = get_amount_in_rub(transaction)

        # Assert
        self.assertIsNone(result)

    # Тест 10: Отсутствие кода валюты (используется RUB по умолчанию)
    def test_missing_currency_code_uses_rub_default(self):
        """Тест: отсутствие кода валюты использует RUB по умолчанию"""
        # Arrange
        transaction = {
            "id": 10,
            "operationAmount": {
                "amount": "500.00",
                "currency": {
                    "name": "рубль"
                    # Нет code
                }
            }
        }

        # Act
        result = get_amount_in_rub(transaction)

        # Assert
        self.assertEqual(result, 500.0)

    # Тест 11: Пустая сумма
    def test_empty_amount_string_returns_zero(self):
        """Тест: пустая строка суммы возвращает 0"""
        # Arrange
        transaction = {
            "id": 11,
            "operationAmount": {
                "amount": "",
                "currency": {
                    "code": "RUB",
                    "name": "рубль"
                }
            }
        }

        # Act
        result = get_amount_in_rub(transaction)

        # Assert
        self.assertEqual(result, 0.0)

    # Тест 12: Нулевая сумма
    def test_zero_amount_returns_zero(self):
        """Тест: нулевая сумма возвращает 0"""
        # Arrange
        transaction = {
            "id": 12,
            "operationAmount": {
                "amount": "0.00",
                "currency": {
                    "code": "RUB",
                    "name": "рубль"
                }
            }
        }

        # Act
        result = get_amount_in_rub(transaction)

        # Assert
        self.assertEqual(result, 0.0)

    # Тест 13: Валюта в нижнем регистре
    def test_lowercase_currency_code_works(self):
        """Тест: код валюты в нижнем регистре работает корректно"""
        # Arrange
        transaction = {
            "id": 13,
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "rub",  # нижний регистр
                    "name": "рубль"
                }
            }
        }

        # Act
        result = get_amount_in_rub(transaction)

        # Assert
        self.assertEqual(result, 100.0)

    # Тест 14: Отрицательная сумма
    def test_negative_amount_works(self):
        """Тест: отрицательная сумма работает корректно"""
        # Arrange
        transaction = {
            "id": 14,
            "operationAmount": {
                "amount": "-100.50",
                "currency": {
                    "code": "RUB",
                    "name": "рубль"
                }
            }
        }

        # Act
        result = get_amount_in_rub(transaction)

        # Assert
        self.assertEqual(result, -100.5)

    # Тест 15: Очень большая сумма
    @patch('src.external_api.os.getenv')
    @patch('src.external_api.requests.get')
    def test_very_large_amount_converts(self, mock_requests_get, mock_getenv):
        """Тест: очень большая сумма корректно конвертируется"""
        # Arrange
        transaction = {
            "id": 15,
            "operationAmount": {
                "amount": "9999999.99",
                "currency": {
                    "code": "USD",
                    "name": "доллар США"
                }
            }
        }

        mock_getenv.return_value = "test_api_key"

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "success": True,
            "result": 749999999.25  # 9999999.99 * 75.0
        }
        mock_requests_get.return_value = mock_response

        # Act
        result = get_amount_in_rub(transaction)

        # Assert
        self.assertEqual(result, 749999999.25)


if __name__ == '__main__':
    unittest.main(verbosity=2)