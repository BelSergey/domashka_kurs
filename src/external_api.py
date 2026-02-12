import os
from typing import Dict, Optional

import requests
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, RequestException, Timeout

load_dotenv()


def get_amount_in_rub(transaction: Dict) -> Optional[float]:
    """Функция для конвертации суммы транзакции в рубли."""
    try:
        if "operationAmount" not in transaction:
            print(f"Ошибка: транзакция {transaction.get('id', 'unknown')} не содержит operationAmount")
            return None

        operation_amount = transaction.get("operationAmount", {})
        amount_str = operation_amount.get("amount", "")
        amount = 0.0 if amount_str == "" else float(amount_str)

        currency_info = operation_amount.get("currency", {})
        currency = str(currency_info.get("code", "RUB")).upper()

        if currency == "RUB":
            return round(amount, 2)

        if currency not in ["USD", "EUR"]:
            print(f"Неподдерживаемая валюта: {currency}")
            return None

        api_key = os.getenv("exchange_rates_data_api_key")
        if not api_key:
            print("Ошибка: API ключ не найден. Проверьте файл .env")
            return None

        params: dict[str, str | float | int] = {
            "from": currency,
            "to": "RUB",
            "amount": amount
        }
        response = requests.get(
            "https://api.apilayer.com/exchangerates_data/convert",
            headers={"apikey": api_key},
            params=params,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if data.get("success", False):
            return round(data.get("result", 0), 2)
        else:
            print(f"API вернуло ошибку: {data.get('error', {}).get('info', 'Unknown error')}")
            return None

    except (RequestException, ConnectionError, Timeout, ValueError, TypeError) as e:
        print(f"Ошибка при конвертации: {e}")
        return None
