import unittest
from unittest.mock import patch, mock_open, MagicMock
import json

from requests import Timeout,ConnectionError

from src.external_api import get_amount_in_rub
from src.utils.json_data_extractor import transaction_data_extractor


class TestGetAmountInRub(unittest.TestCase):
    """Тесты для функции get_amount_in_rub"""

    @patch('src.external_api.os.getenv')
    @patch('src.external_api.requests.get')
    def test_get_amount_in_rub_rub_currency(self, mock_requests_get, mock_getenv):
        """Тест: транзакция уже в рублях"""
        transaction = {
            "id": 1,
            "operationAmount": {
                "amount": "1000.00",
                "currency": {
                    "code": "RUB"
                }
            }
        }

        result = get_amount_in_rub(transaction)

        self.assertEqual(result, 1000.0)
        mock_requests_get.assert_not_called()
        mock_getenv.assert_not_called()

    @patch('src.external_api.os.getenv')
    @patch('src.external_api.requests.get')
    def test_get_amount_in_rub_usd_currency_success(self, mock_requests_get, mock_getenv):
        """Тест: успешная конвертация USD в RUB"""
        transaction = {
            "id": 2,
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "USD"
                }
            }
        }

        mock_getenv.return_value = "test_api_key"

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
            headers={"apikey": "test_api_key"},
            params={"from": "USD", "to": "RUB", "amount": 100.0},
            timeout=10
        )

    @patch('src.external_api.os.getenv')
    @patch('src.external_api.requests.get')
    def test_get_amount_in_rub_eur_currency_success(self, mock_requests_get, mock_getenv):
        """Тест: успешная конвертация EUR в RUB"""
        transaction = {
            "id": 3,
            "operationAmount": {
                "amount": "50.00",
                "currency": {
                    "code": "EUR"
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
        mock_requests_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/convert",
            headers={"apikey": "test_api_key"},
            params={"from": "EUR", "to": "RUB", "amount": 50.0},
            timeout=10
        )

    @patch('src.external_api.os.getenv')
    @patch('src.external_api.requests.get')
    def test_get_amount_in_rub_api_error(self, mock_requests_get, mock_getenv):
        """Тест: API вернуло ошибку"""
        transaction = {
            "id": 4,
            "operationAmount": {
                "amount": "50.00",
                "currency": {
                    "code": "USD"
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
        result = get_amount_in_rub(transaction)

        self.assertIsNone(result)

    @patch('src.external_api.os.getenv')
    def test_get_amount_in_rub_no_api_key(self, mock_getenv):
        """Тест: отсутствует API ключ"""
        transaction = {
            "id": 5,
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "USD"
                }
            }
        }

        mock_getenv.return_value = None

        result = get_amount_in_rub(transaction)

        self.assertIsNone(result)
        mock_getenv.assert_called_once_with("exchange_rates_data_api_key")

    def test_get_amount_in_rub_unsupported_currency(self):
        """Тест: неподдерживаемая валюта"""
        # Arrange
        transaction = {
            "id": 6,
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "GBP"
                }
            }
        }

        result = get_amount_in_rub(transaction)

        self.assertIsNone(result)

    def test_get_amount_in_rub_no_operation_amount(self):
        """Тест: транзакция без operationAmount"""
        transaction = {
            "id": 7,
            "description": "Test transaction"
        }

        result = get_amount_in_rub(transaction)

        self.assertIsNone(result)


    @patch('src.external_api.os.getenv')
    @patch('src.external_api.requests.get')
    def test_get_amount_in_rub_network_error(self, mock_requests_get, mock_getenv):
        """Ошибка сети (requests.exceptions.ConnectionError)"""
        transaction = {
            "id": 8,
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"}
            }
        }
        mock_getenv.return_value = "test_api_key"
        mock_requests_get.side_effect = ConnectionError("Network error")   # 👈 именно из requests

        result = get_amount_in_rub(transaction)
        self.assertIsNone(result)

    @patch('src.external_api.os.getenv')
    @patch('src.external_api.requests.get')
    def test_get_amount_in_rub_timeout_error(self, mock_requests_get, mock_getenv):
        """Таймаут (requests.exceptions.Timeout)"""
        transaction = {
            "id": 9,
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"}
            }
        }
        mock_getenv.return_value = "test_api_key"
        mock_requests_get.side_effect = Timeout("Request timeout")   # 👈 из requests

        result = get_amount_in_rub(transaction)
        self.assertIsNone(result)
    def test_get_amount_in_rub_invalid_amount_format(self):
        """Тест: неверный формат суммы"""
        transaction = {
            "id": 10,
            "operationAmount": {
                "amount": "не число",
                "currency": {
                    "code": "RUB"
                }
            }
        }

        result = get_amount_in_rub(transaction)

        self.assertIsNone(result)

    def test_get_amount_in_rub_missing_currency_code(self):
        """Тест: отсутствует код валюты"""
        # Arrange
        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {}
            }
        }

        result = get_amount_in_rub(transaction)

        self.assertEqual(result, 100.0)

    def test_get_amount_in_rub_empty_string_amount(self):
        """Тест: пустая строка в сумме"""
        transaction = {
            "operationAmount": {
                "amount": "",
                "currency": {"code": "RUB"}
            }
        }

        result = get_amount_in_rub(transaction)

        self.assertEqual(result, 0.0)

    @patch('src.external_api.os.getenv')
    @patch('src.external_api.requests.get')
    def test_get_amount_in_rub_zero_amount(self, mock_requests_get, mock_getenv):
        """Тест: нулевая сумма"""
        transaction = {
            "operationAmount": {
                "amount": "0.00",
                "currency": {"code": "USD"}
            }
        }

        mock_getenv.return_value = "test_api_key"

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "success": True,
            "result": 0.0
        }
        mock_requests_get.return_value = mock_response

        result = get_amount_in_rub(transaction)

        self.assertEqual(result, 0.0)


class TestTransactionDataExtractor(unittest.TestCase):
    """Тесты для функции transaction_data_extractor"""

    @patch('src.utils.json_data_extractor.os.path.exists')
    @patch('src.utils.json_data_extractor.os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_transaction_data_extractor_success(self, mock_file, mock_getsize, mock_exists):
        """Тест: успешное чтение JSON файла"""
        test_data = [
            {
                "id": 441945886,
                "state": "EXECUTED",
                "operationAmount": {
                    "amount": "31957.58",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                }
            }
        ]

        mock_exists.return_value = True
        mock_getsize.return_value = 100
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(test_data)

        result = transaction_data_extractor("test.json")

        self.assertEqual(result, test_data)
        mock_exists.assert_called_once_with("test.json")
        mock_getsize.assert_called_once_with("test.json")
        mock_file.assert_called_once_with("test.json", "r", encoding="utf-8")

    @patch('src.utils.json_data_extractor.os.path.exists')
    def test_transaction_data_extractor_file_not_found(self, mock_exists):
        """Тест: файл не найден"""
        mock_exists.return_value = False

        result = transaction_data_extractor("nonexistent.json")

        self.assertEqual(result, [])
        mock_exists.assert_called_once_with("nonexistent.json")

    @patch('src.utils.json_data_extractor.os.path.exists')
    @patch('src.utils.json_data_extractor.os.path.getsize')
    def test_transaction_data_extractor_empty_file(self, mock_getsize, mock_exists):
        """Тест: пустой файл"""
        mock_exists.return_value = True
        mock_getsize.return_value = 0

        result = transaction_data_extractor("empty.json")

        self.assertEqual(result, [])
        mock_exists.assert_called_once_with("empty.json")
        mock_getsize.assert_called_once_with("empty.json")

    @patch('src.utils.json_data_extractor.os.path.exists')
    @patch('src.utils.json_data_extractor.os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_transaction_data_extractor_json_decode_error(self, mock_file, mock_getsize, mock_exists):
        """Тест: ошибка декодирования JSON"""
        mock_exists.return_value = True
        mock_getsize.return_value = 100

        mock_file.return_value.__enter__.side_effect = json.JSONDecodeError(
            "Invalid JSON", "test.json", 0
        )

        result = transaction_data_extractor("invalid.json")

        self.assertEqual(result, [])

    @patch('src.utils.json_data_extractor.os.path.exists')
    @patch('src.utils.json_data_extractor.os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_transaction_data_extractor_not_list(self, mock_file, mock_getsize, mock_exists):
        """Тест: данные не являются списком"""
        test_data = {"id": 1, "amount": 100}

        mock_exists.return_value = True
        mock_getsize.return_value = 100
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(test_data)

        result = transaction_data_extractor("not_list.json")

        self.assertEqual(result, [])

    @patch('src.utils.json_data_extractor.os.path.exists')
    @patch('src.utils.json_data_extractor.os.path.getsize')
    def test_transaction_data_extractor_permission_error(self, mock_getsize, mock_exists):
        """Тест: нет прав на чтение файла"""
        # Arrange
        mock_exists.return_value = True
        mock_getsize.return_value = 100

        with patch('builtins.open', side_effect=PermissionError("Access denied")):
            result = transaction_data_extractor("protected.json")

        self.assertEqual(result, [])

    @patch('src.utils.json_data_extractor.os.path.exists')
    @patch('src.utils.json_data_extractor.os.path.getsize')
    @patch('builtins.open')
    def test_transaction_data_extractor_unexpected_error(self, mock_file, mock_getsize, mock_exists):
        """Тест: неожиданная ошибка"""
        mock_exists.return_value = True
        mock_getsize.return_value = 100
        mock_file.side_effect = ValueError("Unexpected error")

        result = transaction_data_extractor("error.json")

        self.assertEqual(result, [])

    @patch('src.utils.json_data_extractor.os.path.exists')
    @patch('src.utils.json_data_extractor.os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    def test_transaction_data_extractor_multiple_transactions(self, mock_file, mock_getsize, mock_exists):
        """Тест: чтение файла с несколькими транзакциями"""
        test_data = [
            {
                "id": 441945886,
                "state": "EXECUTED",
                "operationAmount": {
                    "amount": "31957.58",
                    "currency": {"code": "RUB"}
                }
            },
            {
                "id": 41428829,
                "state": "EXECUTED",
                "operationAmount": {
                    "amount": "8221.37",
                    "currency": {"code": "USD"}
                }
            },
            {
                "id": 939719570,
                "state": "EXECUTED",
                "operationAmount": {
                    "amount": "9824.07",
                    "currency": {"code": "USD"}
                }
            }
        ]

        mock_exists.return_value = True
        mock_getsize.return_value = 500
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(test_data)

        result = transaction_data_extractor("multiple.json")

        self.assertEqual(len(result), 3)
        self.assertEqual(result, test_data)

if __name__ == '__main__':
    unittest.main(verbosity=2)