from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from widget import mask_account_card
from  processing import filter_by_state, sort_by_date, filter_by_description, count_operations_by_categories
from utils.json_data_extractor import transaction_data_extractor as tde
from utils.csv_excel_data_extractor import data_extractor as de

BASE_DIR = Path(__file__).resolve().parent.parent


def normalize_operation(op: Dict[str, Any]) -> Dict[str, Any]:
    """
    Приводит операцию к единому плоскому формату:
    ключи 'amount', 'currency_code', 'currency_name' на верхнем уровне.
    Если операция уже плоская, возвращается без изменений.
    """
    if 'amount' in op and ('currency_code' in op or 'currency_name' in op):
        return op

    if 'operationAmount' in op:
        op_amount = op['operationAmount']
        amount = op_amount.get('amount', '0')
        currency = op_amount.get('currency', {})
        currency_code = currency.get('code', '')
        currency_name = currency.get('name', '')

        new_op = {k: v for k, v in op.items() if k != 'operationAmount'}
        new_op['amount'] = amount
        new_op['currency_code'] = currency_code
        new_op['currency_name'] = currency_name
        return new_op
    return op

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

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ").strip()

    # Загружаем данные в зависимости от выбора
    data = []
    if choice == '1':
        print("Для обработки выбран JSON-файл.")
        raw_data = tde(BASE_DIR / "data/operations.json")
        data = [normalize_operation(op) for op in raw_data]
    elif choice == '2':
        print("Для обработки выбран CSV-файл.")
        data = de(BASE_DIR / "data/operations.csv")
    elif choice == '3':
        print("Для обработки выбран XLSX-файл.")
        data = de(BASE_DIR / "data/operations_excel.xlsx")
    else:
        print("Неверный выбор. Завершение программы.")
        return

    if not data:
        print("Не удалось загрузить данные. Программа завершена.")
        return

    # Запрос статуса
    valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}
    while True:
        status_input = input("Введите статус, по которому необходимо выполнить фильтрацию.\n"
                             "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
                             "Пользователь: ").strip()
        if status_input.upper() in valid_statuses:
            break
        print(f"Статус операции \"{status_input}\" недоступен.")

    # Фильтрация по статусу
    filtered_data = filter_by_state(data, status_input)
    print(f"Операции отфильтрованы по статусу \"{status_input}\"")

    if not filtered_data:
        print("Не найдено ни одной транзакции с таким статусом.")
        return
    sort_answer = input("Отсортировать операции по дате? Да/Нет\nПользователь: ").strip().lower()
    if sort_answer in ('да', 'yes', 'y'):
        order = input("Отсортировать по возрастанию или по убыванию?\nПользователь: ").strip().lower()
        reverse = order in ('убыванию', 'убывание', 'desc', 'по убыванию')
        filtered_data = sort_by_date(filtered_data, reverse=reverse)

    rub_answer = input("Выводить только рублевые транзакции? Да/Нет\nПользователь: ").strip().lower()
    if rub_answer in ('да', 'yes', 'y'):
        filtered_data = [op for op in filtered_data if op.get('currency_code') == 'RUB']

    word_answer = input(
        "Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: ").strip().lower()
    if word_answer in ('да', 'yes', 'y'):
        search_word = input("Введите слово для поиска: ").strip()
        filtered_data = filter_by_description(filtered_data, search_word)

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
