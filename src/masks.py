import logging
import os

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
LOG_FILE = os.path.join(LOG_DIR, "masks.log")

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты. Формат: XXXX XX** **** XXXX."""
    logger.info(f"Начало маскирования карты. Входные данные: {card_number}")

    try:
        cleaned_number = "".join(filter(str.isdigit, card_number))

        if len(cleaned_number) != 16:
            error_msg = f"Номер карты должен содержать 16 цифр, получено {len(cleaned_number)}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        first_part = cleaned_number[:4]
        second_part = cleaned_number[4:6]
        last_part = cleaned_number[-4:]
        masked_card = f"{first_part} {second_part}** **** {last_part}"

        logger.debug(f"Результат маскирования: {masked_card}")
        return masked_card

    except Exception:
        logger.exception("Ошибка при маскировании карты")
        raise


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета. Формат: **XXXX."""
    logger.info(f"Начало маскирования счета. Входные данные: {account_number}")

    try:
        cleaned_number = "".join(filter(str.isdigit, account_number))

        if len(cleaned_number) < 4:
            error_msg = f"Номер счета должен содержать минимум 4 цифры, получено {len(cleaned_number)}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        last_four_digits = cleaned_number[-4:]
        masked_account = f"**{last_four_digits}"

        logger.debug(f"Результат маскирования счета: {masked_account}")
        return masked_account

    except Exception:
        logger.exception("Ошибка при маскировании счета")
        raise
