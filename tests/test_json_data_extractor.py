import json
import os
import unittest
from unittest.mock import mock_open, patch

from src.utils.json_data_extractor import transaction_data_extractor


class TestTransactionDataExtractor(unittest.TestCase):
    """Тесты для функции transaction_data_extractor."""

    @patch("src.utils.json_data_extractor.os.path.exists")
    @patch("src.utils.json_data_extractor.os.path.getsize")
    @patch("builtins.open", new_callable=mock_open)
    def test_successful_read_valid_json(self, mock_file, mock_getsize, mock_exists):
        """Корректный JSON-файл -> возвращает список транзакций."""
        test_data = [
            {"id": 1, "operationAmount": {"amount": "100", "currency": {"code": "RUB"}}},
            {"id": 2, "operationAmount": {"amount": "200", "currency": {"code": "USD"}}},
        ]
        mock_exists.return_value = True
        mock_getsize.return_value = 1024
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(test_data)

        result = transaction_data_extractor("test.json")
        self.assertEqual(result, test_data)

    @patch("src.utils.json_data_extractor.os.path.exists")
    def test_file_not_found(self, mock_exists):
        """Файл не существует -> пустой список."""
        mock_exists.return_value = False
        result = transaction_data_extractor("nonexistent.json")
        self.assertEqual(result, [])

    @patch("src.utils.json_data_extractor.os.path.exists")
    @patch("src.utils.json_data_extractor.os.path.getsize")
    def test_empty_file(self, mock_getsize, mock_exists):
        """Файл пустой (размер 0) -> пустой список."""
        mock_exists.return_value = True
        mock_getsize.return_value = 0
        result = transaction_data_extractor("empty.json")
        self.assertEqual(result, [])

    @patch("src.utils.json_data_extractor.os.path.exists")
    @patch("src.utils.json_data_extractor.os.path.getsize")
    @patch("builtins.open", new_callable=mock_open)
    def test_json_decode_error(self, mock_file, mock_getsize, mock_exists):
        """Некорректный JSON -> пустой список."""
        mock_exists.return_value = True
        mock_getsize.return_value = 100
        mock_file.return_value.__enter__.return_value.read.return_value = "{invalid json}"
        with patch("json.load", side_effect=json.JSONDecodeError("Mock error", "", 0)):
            result = transaction_data_extractor("bad.json")
            self.assertEqual(result, [])

    @patch("src.utils.json_data_extractor.os.path.exists")
    @patch("src.utils.json_data_extractor.os.path.getsize")
    @patch("builtins.open", new_callable=mock_open)
    def test_data_not_list(self, mock_file, mock_getsize, mock_exists):
        """JSON содержит словарь, а не список -> пустой список."""
        test_data = {"id": 1, "amount": 100}
        mock_exists.return_value = True
        mock_getsize.return_value = 100
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(test_data)

        result = transaction_data_extractor("not_list.json")
        self.assertEqual(result, [])

    @patch("src.utils.json_data_extractor.os.path.exists")
    @patch("src.utils.json_data_extractor.os.path.getsize")
    def test_permission_error(self, mock_getsize, mock_exists):
        """Нет прав на чтение файла -> пустой список."""
        mock_exists.return_value = True
        mock_getsize.return_value = 100
        with patch("builtins.open", side_effect=PermissionError("Access denied")):
            result = transaction_data_extractor("protected.json")
            self.assertEqual(result, [])

    @patch("src.utils.json_data_extractor.os.path.exists")
    @patch("src.utils.json_data_extractor.os.path.getsize")
    @patch("builtins.open")
    def test_unexpected_error(self, mock_open, mock_getsize, mock_exists):
        """Любая другая ошибка при открытии/чтении -> пустой список."""
        mock_exists.return_value = True
        mock_getsize.return_value = 100
        mock_open.side_effect = ValueError("Something went wrong")
        result = transaction_data_extractor("error.json")
        self.assertEqual(result, [])

    @patch("src.utils.json_data_extractor.os.path.exists")
    @patch("src.utils.json_data_extractor.os.path.basename")
    @patch("src.utils.json_data_extractor.print")
    def test_error_message_uses_basename(self, mock_print, mock_basename, mock_exists):
        """В сообщении об ошибке используется только имя файла, а не полный путь."""
        mock_exists.return_value = False
        mock_basename.return_value = "myfile.json"
        transaction_data_extractor(r"C:\Users\79045\PycharmProjects\domashka_kurs\mylog.txt")
        mock_print.assert_called_with("Файл myfile.json не найден!")

    @patch("src.utils.json_data_extractor.os.path.exists")
    @patch("src.utils.json_data_extractor.os.path.getsize")
    @patch("builtins.open", new_callable=mock_open)
    def test_large_file(self, mock_file, mock_getsize, mock_exists):
        """Успешное чтение файла с 1000 транзакций."""
        test_data = [{"id": i, "amount": i * 100} for i in range(1000)]
        mock_exists.return_value = True
        mock_getsize.return_value = 50000
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(test_data)

        result = transaction_data_extractor("large.json")
        self.assertEqual(len(result), 1000)
        self.assertEqual(result[0]["id"], 0)
        self.assertEqual(result[999]["id"], 999)


if __name__ == "__main__":
    unittest.main(verbosity=2)
