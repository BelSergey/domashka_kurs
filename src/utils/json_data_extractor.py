import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "json_data_extractor.log"

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)


def transaction_data_extractor(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл с транзакциями и возвращает список словарей.
    В случае ошибок возвращает пустой список, записывая детали в лог.
    """
    logger.info(f"Начало чтения файла: {file_path}")

    if not os.path.exists(file_path):
        error_msg = f"Файл {os.path.basename(file_path)} не найден"
        logger.error(error_msg)
        print(error_msg)
        return []

    if os.path.getsize(file_path) == 0:
        warning_msg = f"Файл {os.path.basename(file_path)} пустой"
        logger.warning(warning_msg)
        print(warning_msg)
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            transaction_data = json.load(file)
            if not isinstance(transaction_data, list):
                type_error_msg = f"Данные в файле не являются списком. Тип данных: {type(transaction_data)}"
                logger.error(type_error_msg)
                print(type_error_msg)
                return []

            logger.info(f"Файл успешно прочитан. Количество транзакций: {len(transaction_data)}")
            return transaction_data

    except json.JSONDecodeError as e:
        logger.exception(f"Ошибка декодирования JSON в файле {file_path}")
        print(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
    except PermissionError as e:
        logger.exception(f"Нет прав на чтение файла {file_path}")
        print(f"Нет прав на чтение файла {file_path}: {e}")
        return []
    except Exception as e:
        logger.exception(f"Неожиданная ошибка при чтении файла {file_path}")
        print(f"Неожиданная ошибка при чтении файла {file_path}: {e}")
        return []
