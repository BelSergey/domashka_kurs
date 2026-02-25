from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(input_string: str) -> str:
    """Маскирует номер карты или счета в строке."""
    if not input_string:
        return ""

    parts = input_string.strip().split()
    if len(parts) < 2:
        return ""

    number = parts[-1]
    name = " ".join(parts[:-1])

    try:
        if name.startswith(("Visa", "Maestro", "MasterCard")):
            masked = get_mask_card_number(number)
            return f"{name} {masked}"
        elif name == "Счет":
            masked = get_mask_account(number)
            return f"{name} {masked}"
        else:
            return ""
    except Exception:
        return ""


def get_date(date_string: str) -> str:
    """Преобразует строку с датой в формате ISO 8601 в строку в формате "ДД.ММ.ГГГГ"""
    if not date_string:
        return ""

    if "T" in date_string:
        date_string = date_string.split("T")[0]

    try:
        dt = datetime.strptime(date_string, "%Y-%m-%d")
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        return ""
