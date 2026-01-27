"""
Общие фикстуры для тестов
"""
import pytest
from typing import List, Dict, Any


# Фикстуры для масок карт
@pytest.fixture(params=[
    ("7000792289606361", "7000 79** **** 6361"),
    ("1596837868705199", "1596 83** **** 5199"),
    ("7158300734726758", "7158 30** **** 6758"),
    ("1234567812345678", "1234 56** **** 5678"),
    ("0000000000000000", "0000 00** **** 0000"),
    ("9999999999999999", "9999 99** **** 9999"),
])
def valid_card_number_pair(request):
    """Фикстура с валидными номерами карт и ожидаемыми результатами"""
    return request.param


@pytest.fixture(params=[
    ("123456789012345", "15 цифр"),
    ("12345678901234567", "17 цифр"),
    ("", "пустая строка"),
    ("abcd-efgh-ijkl-mnop", "не цифры"),
])
def invalid_card_number(request):
    """Фикстура с невалидными номерами карт"""
    return request.param


@pytest.fixture(params=[
    ("7000 7922 8960 6361", "7000 79** **** 6361"),
    ("7000-7922-8960-6361", "7000 79** **** 6361"),
    ("7000 7922-8960 6361", "7000 79** **** 6361"),
    ("7000.7922.8960.6361", "7000 79** **** 6361"),
])
def formatted_card_number_pair(request):
    """Фикстура с отформатированными номерами карт"""
    return request.param


# Фикстуры для масок счетов
@pytest.fixture(params=[
    ("73654108430135874305", "**4305"),
    ("35383033474447895560", "**5560"),
    ("1234", "**1234"),
    ("9876543210", "**3210"),
    ("00000000000000000000", "**0000"),
    ("99999999999999999999", "**9999"),
])
def valid_account_number_pair(request):
    """Фикстура с валидными номерами счетов"""
    return request.param


@pytest.fixture(params=[
    ("123", "3 цифры"),
    ("12", "2 цифры"),
    ("", "пустая строка"),
    ("abc", "не цифры"),
])
def invalid_account_number(request):
    """Фикстура с невалидными номерами счетов"""
    return request.param


@pytest.fixture(params=[
    ("7365 4108 4301 3587 4305", "**4305"),
    ("7365-4108-4301-3587-4305", "**4305"),
    ("7365.4108.4301.3587.4305", "**4305"),
    ("7365 4108-4301 3587.4305", "**4305"),
])
def formatted_account_number_pair(request):
    """Фикстура с отформатированными номерами счетов"""
    return request.param


# Фикстуры для операций
@pytest.fixture
def sample_operations():
    """Фикстура с примером операций"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01", "amount": 100},
        {"id": 2, "state": "CANCELED", "date": "2023-01-02", "amount": 200},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-03", "amount": 300},
        {"id": 4, "state": "PENDING", "date": "2023-01-04", "amount": 400},
        {"id": 5, "state": "EXECUTED", "date": "2023-01-05", "amount": 500},
        {"id": 6, "date": "2023-01-06", "amount": 600},
        {"id": 7, "state": None, "date": "2023-01-07", "amount": 700},
        {"id": 8, "state": "executed", "date": "2023-01-08", "amount": 800},
    ]


@pytest.fixture
def operations_for_sorting():
    """Фикстура с операциями для сортировки"""
    return [
        {"id": 1, "date": "2023-01-01", "amount": 100},
        {"id": 2, "date": "2023-01-03", "amount": 200},
        {"id": 3, "date": "2023-01-02", "amount": 300},
        {"id": 4, "date": "2022-12-31", "amount": 400},
        {"id": 5, "amount": 500},
        {"id": 6, "date": "2023-01-01T12:00:00", "amount": 600},
        {"id": 7, "date": "2023-01-01T08:00:00", "amount": 700},
    ]


@pytest.fixture(params=[
    ("EXECUTED", [1, 3, 5]),
    ("CANCELED", [2]),
    ("PENDING", [4]),
    ("NONEXISTENT", []),
    ("executed", [8]),
    ("", []),
])
def state_and_expected_ids(request):
    """Фикстура с состояниями и ожидаемыми ID"""
    return request.param


@pytest.fixture(params=[
    (True, 2),   # reverse=True, ожидаемый первый ID с датой
    (False, 4),  # reverse=False, ожидаемый первый ID с датой
])
def reverse_and_first_id(request):
    """Фикстура с направлением сортировки и ожидаемым первым ID"""
    return request.param


# Фикстуры для виджета
@pytest.fixture(params=[
    ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ("Visa Classic 1234567812345678", "Visa Classic 1234 56** **** 5678"),
    ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
    ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
    ("MasterCard Platinum 1234567812345678", "MasterCard Platinum 1234 56** **** 5678"),
    ("Visa 0000000000000000", "Visa 0000 00** **** 0000"),
])
def valid_card_string_pair(request):
    """Фикстура с валидными строками карт"""
    return request.param


@pytest.fixture(params=[
    ("Счет 73654108430135874305", "Счет **4305"),
    ("Счет 35383033474447895560", "Счет **5560"),
    ("Счет 12345678901234567890", "Счет **7890"),
    ("Счет 00000000000000000000", "Счет **0000"),
])
def valid_account_string_pair(request):
    """Фикстура с валидными строками счетов"""
    return request.param


@pytest.fixture(params=[
    ("American Express 378282246310005", ""),
    ("МИР 1234567812345678", ""),
    ("Visa", ""),
    ("Счет", ""),
    ("", ""),
    ("   ", ""),
    ("Some Unknown Card 1234567812345678", ""),
])
def invalid_string_pair(request):
    """Фикстура с невалидными строками"""
    return request.param


@pytest.fixture(params=[
    ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ("Visa Classic 1234-5678-9012-3456", "Visa Classic 1234 56** **** 3456"),
    ("Счет 73654108430135874305", "Счет **4305"),
    ("Счет 7365-4108-4301-3587-4305", "Счет **4305"),
])
def formatted_string_pair(request):
    """Фикстура с отформатированными строками (без пробелов в номерах)"""
    return request.param


@pytest.fixture(params=[
    ("2023-01-15T12:30:45", "15.01.2023"),
    ("2023-01-15", "15.01.2023"),
    ("2024-02-29T00:00:00", "29.02.2024"),
    ("2000-01-01T23:59:59", "01.01.2000"),
    ("1999-12-31", "31.12.1999"),
    ("2030-12-31T12:00:00", "31.12.2030"),
    ("1900-01-01", "01.01.1900"),
])
def valid_date_pair(request):
    """Фикстура с валидными датами"""
    return request.param


@pytest.fixture(params=[
    ("", ""),
    ("2023-13-45", ""),
    ("15/01/2023", ""),
    ("2023-01", ""),
    ("not a date", ""),
    ("123456", ""),
])
def invalid_date_pair(request):
    """Фикстура с невалидными датами"""
    return request.param


@pytest.fixture(params=[
    ("2023-01-15T12:30:45+03:00", "15.01.2023"),
    ("2023-01-15T12:30:45Z", "15.01.2023"),
    ("2023-01-15T12:30:45+05:30", "15.01.2023"),
    ("2023-01-15T12:30:45-08:00", "15.01.2023"),
])
def date_with_timezone_pair(request):
    """Фикстура с датами с часовым поясом"""
    return request.param


@pytest.fixture(params=[
    ("2023-01-15T12:30:45.123", "15.01.2023"),
    ("2023-01-15T12:30:45.123456", "15.01.2023"),
    ("2023-01-15T12:30:45.000", "15.01.2023"),
])
def date_with_milliseconds_pair(request):
    """Фикстура с датами с миллисекундами"""
    return request.param


# Интеграционные фикстуры
@pytest.fixture
def complex_operations():
    """Фикстура со сложными операциями для интеграционных тестов"""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-15T12:30:45",
            "description": "Оплата услуг",
            "from": "Visa Platinum 7000792289606361",
            "to": "Счет 73654108430135874305",
            "operationAmount": {"amount": "1000.00", "currency": {"name": "RUB"}}
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2023-01-10T08:15:00",
            "description": "Перевод другу",
            "from": "Maestro 1596837868705199",
            "to": "Счет 35383033474447895560",
            "operationAmount": {"amount": "500.00", "currency": {"name": "USD"}}
        },
        {
            "id": 3,
            "state": "CANCELED",
            "date": "2023-01-20T18:45:30",
            "description": "Возврат средств",
            "from": "MasterCard 7158300734726758",
            "to": "Visa Classic 1234567812345678",
            "operationAmount": {"amount": "200.00", "currency": {"name": "EUR"}}
        },
        {
            "id": 4,
            "state": "PENDING",
            "date": "2023-01-05T10:00:00",
            "description": "Запрос на оплату",
            "from": "Счет 12345678901234567890",
            "to": "Счет 09876543210987654321",
            "operationAmount": {"amount": "1500.00", "currency": {"name": "RUB"}}
        },
    ]


@pytest.fixture
def edge_case_operations():
    """Фикстура с пограничными случаями операций"""
    return [
        {"id": 1},
        {"state": "EXECUTED"},
        {"date": "2023-01-01"},
        {"from": "Visa 1234567812345678"},
        {"to": "Счет 12345678901234567890"},
        {},
    ]

@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с примером транзакций."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "RUB", "code": "RUB"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "CANCELED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 596171168,
            "state": "EXECUTED",
            "date": "2018-07-11T02:26:18.671407",
            "operationAmount": {
                "amount": "79931.03",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Открытие вклада",
            "to": "Счет 72082042523231456215",
        },
    ]


@pytest.fixture
def empty_transactions() -> List[Dict[str, Any]]:
    """Фикстура с пустым списком транзакций."""
    return []


@pytest.fixture
def single_transaction() -> List[Dict[str, Any]]:
    """Фикстура с одной транзакцией."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-01-01T00:00:00.000000",
            "operationAmount": {
                "amount": "1000.00",
                "currency": {"name": "EUR", "code": "EUR"},
            },
            "description": "Тестовая транзакция",
        }
    ]