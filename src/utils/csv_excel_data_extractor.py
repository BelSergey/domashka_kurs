import os
from pathlib import Path
import logging
from typing import List, Dict, Any, Optional
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "csv_excel_data_extractor.log"

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)


def data_extractor(file_path: str, separator: str = ";",  sheet_name: str | int = 0) -> Optional[List[Dict[str, Any]]]:
    """ Читает CSV или Excel файл с транзакциями и возвращает список словарей. """

    logger.info(f"Начало чтения файла: {file_path}")

    if not os.path.exists(file_path):
        logger.error(f"Файл {os.path.basename(file_path)} не найден")
        return None

    if os.path.getsize(file_path) == 0:
        logger.warning(f"Файл {os.path.basename(file_path)} пустой")
        return []

    _, extension = os.path.splitext(file_path)
    extension = extension.lower()

    try:
        if extension == '.csv':
            df = pd.read_csv(file_path, sep=separator)
        elif extension in ('.xlsx', '.xls'):
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            logger.error(f"Неподдерживаемый формат файла: {extension}")
            return []

        records = df.to_dict(orient='records')
        logger.info(f"Успешно прочитано {len(records)} записей из файла {file_path}")
        return records

    except pd.errors.EmptyDataError:
        logger.warning(f"Файл {file_path} не содержит данных")
        return []
    except Exception as e:
        logger.exception(f"Ошибка при чтении файла {file_path}: {e}")
        return []
