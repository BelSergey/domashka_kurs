from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(incoming_data):
    """Маскирует номер карты или счета."""
    if incoming_data is None:
        return ""
    s = str(incoming_data).strip()
    if not s or s.lower() == 'nan':
        return ""


    if s.isdigit():
        if len(s) >= 16:
            return f"{s[:4]} {s[4:6]}** **** {s[-4:]}"
        else:
            return s

    parts = s.split()
    if len(parts) < 2:
        if s.startswith("Счет") and len(s) > 5:
            account = s[5:].strip()
            if account.isdigit() and len(account) >= 4:
                return f"Счет **{account[-4:]}"
        return s

    card_name_parts = parts[:-1]
    number = parts[-1]

    try:
        if parts[0] in ["Visa", "Maestro", "MasterCard"]:
            card_name = " ".join(card_name_parts)
            return f"{card_name} {get_mask_card_number(number)}"
        elif parts[0] == "Счет":
            return f"{parts[0]} {get_mask_account(number)}"
    except ValueError:
        pass

    return s


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
