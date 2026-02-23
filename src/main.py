from datetime import datetime
from typing import List, Dict, Any

from widget import mask_account_card
def format_output(operation: Dict[str, Any]) -> str:
    """Форматирует одну операцию для вывода."""

    date_iso = operation.get('date', '')
    try:
        dt = datetime.fromisoformat(date_iso.replace('Z', '+00:00'))
        date_str = dt.strftime('%d.%m.%Y')
    except (ValueError, TypeError):
        date_str = '??.??.????'

    description = operation.get('description', 'Без описания')

    from_str = mask_account_card(operation.get('from', ''))
    to_str = mask_account_card(operation.get('to', ''))

    amount = operation.get('amount', '0')
    currency = operation.get('currency_code', operation.get('currency_name', '')).upper()
    if currency == 'RUB':
        currency = 'руб.'
    elif currency == 'USD':
        currency = 'USD'
    elif currency == 'EUR':
        currency = 'EUR'
    lines = [
        f"{date_str} {description}",
        f"{from_str} -> {to_str}" if from_str else f"-> {to_str}",
        f"Сумма: {amount} {currency}"
    ]
    return '\n'.join(lines)



def main():
    return