from masks import get_mask_account, get_mask_card_number
from datetime import datetime


def mask_account_card(incoming_string: str) -> str:
    """Функция обрабатывает информацию о картах и счетах"""
    if not incoming_string:
        return ""

    parts = incoming_string.split(" ")
    if len(parts) < 2:
        return ""

    card_name_parts = parts[:-1]
    number = parts[-1]

    if parts[0] in ["Visa", "Maestro", "MasterCard"]:
        card_name = " ".join(card_name_parts)
        return f"{card_name} {get_mask_card_number(number)}"
    elif parts[0] == "Счет":
        return f"{parts[0]} {get_mask_account(number)}"

    return ""


def get_date(date_string: str) -> str:
    """Преобразует строку с датой в формате ISO 8601 в строку в формате "ДД.ММ.ГГГГ"""
    if not date_string:
        return ""

    if 'T' in date_string:
        date_string = date_string.split('T')[0]

    try:
        dt = datetime.strptime(date_string, "%Y-%m-%d")
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        return ""

