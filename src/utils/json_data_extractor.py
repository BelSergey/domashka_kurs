import json
import os
from typing import Any, Dict, List


def transaction_data_extractor(file_path: str) -> List[Dict[str, Any]]:
    """Функция для получения данных о транзакциях из json файла"""

    if not os.path.exists(file_path):
        print(f"Файл {os.path.basename(file_path)} не найден!")
        return []

    if os.path.getsize(file_path) == 0:
        print(f"Файл {os.path.basename(file_path)} пустой!")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            transaction_data = json.load(file)
            if not isinstance(transaction_data, list):
                print(f"Данные в файле не являются списком. Тип данных: {type(transaction_data)}")
                return []
            return transaction_data
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
    except PermissionError as e:
        print(f"Нет прав на чтение файла {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Неожиданная ошибка при чтении файла {file_path}: {e}")
        return []

