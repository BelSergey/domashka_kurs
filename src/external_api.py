import os
import requests
from typing import Dict, Optional
from dotenv import load_dotenv
from utils.json_data_extractor import transaction_data_extractor

load_dotenv()


def get_amount_in_rub(transaction: Dict) -> Optional[float]:
    """Функция для конвертации суммы транзакции в рубли"""
    try:
        if "operationAmount" not in transaction:
            print(f"Ошибка: транзакция {transaction.get('id', 'unknown')} не содержит operationAmount")
            return None

        operation_amount = transaction.get("operationAmount", {})
        amount = float(operation_amount.get("amount", 0))
        currency_info = operation_amount.get("currency", {})
        currency = str(currency_info.get("code", "RUB")).upper()

        if currency == "RUB":
            return amount

        if currency not in ["USD", "EUR"]:
            print(f"Неподдерживаемая валюта: {currency}")
            return None

        api_key = os.getenv("exchange_rates_data_api_key")
        if not api_key:
            print("Ошибка: API ключ не найден. Проверьте файл .env")
            return None

        url = "https://api.apilayer.com/exchangerates_data/convert"
        headers = {"apikey": api_key}
        params = {
            "from": currency,
            "to": "RUB",
            "amount": amount
        }

        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("success", False):
            return round(data.get("result", 0), 2)
        else:
            print(f"API вернуло ошибку: {data.get('error', {}).get('info', 'Unknown error')}")
            return None

    except (requests.RequestException, ValueError, TypeError) as e:
        print(f"Ошибка при конвертации: {e}")
        return None


transactions_list = transaction_data_extractor(os.getenv("data_path"))

result = get_amount_in_rub(transactions_list[1])
if result is not None:
    print(f" {result} RUB")
else:
    print("Не удалось конвертировать")