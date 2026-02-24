import builtins
from src.main import format_output, normalize_operation, main


def test_format_output_full(monkeypatch, flat_operation):
    monkeypatch.setattr("src.main.mask_account_card", lambda x: x)
    result = format_output(flat_operation)
    assert "10.01.2023 Перевод" in result
    assert "Счет 1111 -> Карта 2222" in result
    assert "Сумма: 1000 руб." in result

def test_format_output_only_from(monkeypatch):
    monkeypatch.setattr("src.main.mask_account_card", lambda x: x)
    op = {"from": "Счет", "amount": "1", "currency_code": "USD"}
    result = format_output(op)
    assert "Счет ->" in result

def test_format_output_only_to(monkeypatch):
    monkeypatch.setattr("src.main.mask_account_card", lambda x: x)
    op = {"to": "Карта", "amount": "1", "currency_code": "EUR"}
    result = format_output(op)
    assert "Карта" in result

def test_format_output_no_from_to(monkeypatch):
    monkeypatch.setattr("src.main.mask_account_card", lambda x: "")
    op = {"amount": 5.0, "currency_name": "RUB"}
    result = format_output(op)
    assert "Сумма: 5 руб." in result

def test_format_output_bad_date(monkeypatch):
    monkeypatch.setattr("src.main.mask_account_card", lambda x: x)
    op = {"date": "bad-date", "amount": "1", "currency_code": "USD"}
    result = format_output(op)
    assert "??.??.????" in result

def test_normalize_flat(flat_operation):
    assert normalize_operation(flat_operation) == flat_operation

def test_normalize_nested(nested_operation):
    result = normalize_operation(nested_operation)
    assert result["amount"] == "500"
    assert result["currency_code"] == "EUR"
    assert result["currency_name"] == "euro"
    assert "operationAmount" not in result

def test_normalize_other():
    op = {"test": 1}
    assert normalize_operation(op) == op

def test_main_json_full_flow(monkeypatch, input_seq, flat_operation, flat_usd_operation):
    input_seq([
        "1",    # JSON
        "1",    # EXECUTED
        "да",   # sort
        "2",    # desc
        "да",   # rub
        "да",   # word
        "Перевод",
    ])

    data = [flat_operation, flat_usd_operation]

    monkeypatch.setattr("src.main.tde", lambda _: data)
    monkeypatch.setattr("src.main.filter_by_state", lambda d, s: d)
    monkeypatch.setattr("src.main.sort_by_date", lambda d, reverse: d)
    monkeypatch.setattr("src.main.filter_by_description", lambda d, w: [flat_operation])
    monkeypatch.setattr("src.main.mask_account_card", lambda x: x)

    out = []
    monkeypatch.setattr(builtins, "print", lambda *a: out.append(" ".join(map(str, a))))

    main()
    assert any("Всего банковских операций" in x for x in out)

def test_main_csv_none(monkeypatch, input_seq):
    input_seq(["2"])

    monkeypatch.setattr("src.main.de", lambda _: None)
    out = []
    monkeypatch.setattr(builtins, "print", lambda *a: out.append(" ".join(map(str, a))))

    main()
    assert "Не удалось загрузить данные." in out[-1]

def test_main_xlsx_none(monkeypatch, input_seq):
    input_seq(["3"])

    monkeypatch.setattr("src.main.de", lambda _: None)
    out = []
    monkeypatch.setattr(builtins, "print", lambda *a: out.append(" ".join(map(str, a))))

    main()
    assert "Не удалось загрузить данные." in out[-1]

def test_main_invalid_choice(monkeypatch, input_seq):
    input_seq(["9"])
    out = []
    monkeypatch.setattr(builtins, "print", lambda *a: out.append(" ".join(map(str, a))))
    main()
    assert "Неверный выбор" in out[-1]

def test_main_no_filtered(monkeypatch, input_seq):
    input_seq(["1", "1"])
    monkeypatch.setattr("src.main.tde", lambda _: [{"state": "EXECUTED"}])
    monkeypatch.setattr("src.main.filter_by_state", lambda d, s: [])
    out = []
    monkeypatch.setattr(builtins, "print", lambda *a: out.append(" ".join(map(str, a))))
    main()
    assert "Не найдено ни одной транзакции" in out[-1]


def test_main_sort_invalid_then_valid(monkeypatch, input_seq, flat_operation):
    input_seq([
        "1", "1",
        "да",
        "9",
        "1",
        "нет",
        "нет",
    ])

    monkeypatch.setattr("src.main.tde", lambda _: [flat_operation])
    monkeypatch.setattr("src.main.filter_by_state", lambda d, s: d)
    monkeypatch.setattr("src.main.sort_by_date", lambda d, reverse: d)
    monkeypatch.setattr("src.main.mask_account_card", lambda x: x)
    monkeypatch.setattr("src.main.filter_by_description", lambda d, w: d)

    out = []
    monkeypatch.setattr(builtins, "print", lambda *a: out.append(" ".join(map(str, a))))
    main()
    assert any("Распечатываю итоговый список" in x for x in out)