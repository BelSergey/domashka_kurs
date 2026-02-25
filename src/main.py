from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from src.processing import (
    filter_by_description,
    filter_by_state,
    sort_by_date,
)
from src.utils.csv_excel_data_extractor import data_extractor as de
from src.utils.json_data_extractor import transaction_data_extractor as tde
from src.widget import mask_account_card

BASE_DIR = Path(__file__).resolve().parent.parent


def format_output(operation: Dict[str, Any]) -> str:
    """Форматирует одну операцию для вывода."""
    date_iso = operation.get("date", "")
    try:
        dt = datetime.fromisoformat(date_iso.replace("Z", "+00:00"))
        date_str = dt.strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        date_str = "??.??.????"

    description = operation.get("description", "Без описания")
    from_str = mask_account_card(operation.get("from", ""))
    to_str = mask_account_card(operation.get("to", ""))

    amount_raw = operation.get("amount", "0")
    try:
        if isinstance(amount_raw, float) and amount_raw.is_integer():
            amount = str(int(amount_raw))
        elif isinstance(amount_raw, str) and amount_raw.endswith(".0"):
            amount = amount_raw[:-2]
        else:
            amount = str(amount_raw)
    except Exception:
        amount = str(amount_raw)

    currency = operation.get("currency_code", operation.get("currency_name", "")).upper()
    currency_map = {"RUB": "руб.", "USD": "USD", "EUR": "EUR"}
    currency = currency_map.get(currency, currency)

    # Формируем вторую строку
    if from_str and to_str:
        second_line = f"{from_str} -> {to_str}"
    elif from_str:
        second_line = f"{from_str} ->"
    elif to_str:
        second_line = to_str
    else:
        second_line = ""

    lines = [
        f"{date_str} {description}",
        second_line,
        f"Сумма: {amount} {currency}",
    ]
    if not second_line:
        lines.pop(1)
    return "\n".join(lines)


def normalize_operation(op: Dict[str, Any]) -> Dict[str, Any]:
    """Приводит операцию к единому плоскому формату (для JSON с вложенной структурой)."""
    if "amount" in op and ("currency_code" in op or "currency_name" in op):
        return op

    if "operationAmount" in op:
        op_amount = op["operationAmount"]
        amount = op_amount.get("amount", "0")
        currency = op_amount.get("currency", {})
        currency_code = currency.get("code", "")
        currency_name = currency.get("name", "")

        new_op = {k: v for k, v in op.items() if k != "operationAmount"}
        new_op["amount"] = amount
        new_op["currency_code"] = currency_code
        new_op["currency_name"] = currency_name
        return new_op

    return op


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ").strip()

    data: list[dict[str, Any]] = []
    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        raw_data = tde(str(BASE_DIR / "data/operations.json"))
        data = [normalize_operation(op) for op in raw_data]
    elif choice == "2":
        print("Для обработки выбран CSV-файл.")
        result = de(str(BASE_DIR / "data/transactions.csv"))
        if result is None:
            print("Не удалось загрузить данные.")
            return
        data = result
    elif choice == "3":
        result = de(str(BASE_DIR / "data/transactions_excel.xlsx"))
        if result is None:
            print("Не удалось загрузить данные.")
            return
        data = result
    else:
        print("Неверный выбор. Завершение программы.")
        return

    if not data:
        print("Не удалось загрузить данные. Программа завершена.")
        return

    status_map = {"1": "EXECUTED", "2": "CANCELED", "3": "PENDING"}
    while True:
        print("\nВыберите статус операций:")
        print("1. EXECUTED")
        print("2. CANCELED")
        print("3. PENDING")
        choice_status = input("Пользователь: ").strip()
        if choice_status in status_map:
            selected_status = status_map[choice_status]
            break
        print(f"Вариант {choice_status} недоступен.")

    filtered_data = filter_by_state(data, selected_status)
    print(f'Операции отфильтрованы по статусу "{selected_status}"')

    if not filtered_data:
        print("Не найдено ни одной транзакции с таким статусом.")
        return

    sort_answer = input("\nОтсортировать операции по дате? Да/Нет\nПользователь: ").strip().lower()
    if sort_answer in ("да", "yes", "y"):
        order_map = {"1": False, "2": True}
        while True:
            print("Выберите порядок сортировки:")
            print("1. По возрастанию")
            print("2. По убыванию")
            order_choice = input("Пользователь: ").strip()
            if order_choice in order_map:
                reverse = order_map[order_choice]
                break
            print("Неверный ввод. Попробуйте снова.")
        filtered_data = sort_by_date(filtered_data, reverse=reverse)

    rub_answer = input("\nВыводить только рублевые транзакции? Да/Нет\nПользователь: ").strip().lower()
    if rub_answer in ("да", "yes", "y"):
        filtered_data = [op for op in filtered_data if op.get("currency_code") == "RUB"]

    word_answer = (
        input("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: ")
        .strip()
        .lower()
    )
    if word_answer in ("да", "yes", "y"):
        search_word = input("Введите слово для поиска: ").strip()
        filtered_data = filter_by_description(filtered_data, search_word)

    # Вывод результата
    print("\nРаспечатываю итоговый список транзакций...")
    if not filtered_data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(filtered_data)}\n")
        for op in filtered_data:
            print(format_output(op))
            print()


if __name__ == "__main__":
    main()
