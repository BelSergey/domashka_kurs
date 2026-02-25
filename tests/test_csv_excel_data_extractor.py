import os
import pandas as pd
import pytest

from src.utils.csv_excel_data_extractor import data_extractor


def test_file_not_exists(tmp_path):
    file_path = tmp_path / "missing.csv"
    result = data_extractor(str(file_path))
    assert result is None


def test_empty_file(tmp_path):
    file_path = tmp_path / "empty.csv"
    file_path.write_text("", encoding="utf-8")

    result = data_extractor(str(file_path))
    assert result == []


def test_unsupported_extension(tmp_path):
    file_path = tmp_path / "data.txt"
    file_path.write_text("some text", encoding="utf-8")

    result = data_extractor(str(file_path))
    assert result == []


def test_csv_file_reading(tmp_path):
    file_path = tmp_path / "data.csv"
    content = "id;amount\n1;100\n2;200"
    file_path.write_text(content, encoding="utf-8")

    result = data_extractor(str(file_path), separator=";")

    assert result == [
        {"id": 1, "amount": 100},
        {"id": 2, "amount": 200},
    ]


def test_csv_with_custom_separator(tmp_path):
    file_path = tmp_path / "data.csv"
    content = "id,amount\n1,100\n2,200"
    file_path.write_text(content, encoding="utf-8")

    result = data_extractor(str(file_path), separator=",")

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["amount"] == 200


def test_excel_file_reading(tmp_path):
    file_path = tmp_path / "data.xlsx"

    df = pd.DataFrame(
        [
            {"id": 1, "amount": 100},
            {"id": 2, "amount": 200},
        ]
    )
    df.to_excel(file_path, index=False)

    result = data_extractor(str(file_path))

    assert result == [
        {"id": 1, "amount": 100},
        {"id": 2, "amount": 200},
    ]


def test_excel_specific_sheet(tmp_path):
    file_path = tmp_path / "data.xlsx"

    with pd.ExcelWriter(file_path) as writer:
        pd.DataFrame([{"a": 1}]).to_excel(writer, sheet_name="Sheet1", index=False)
        pd.DataFrame([{"b": 2}]).to_excel(writer, sheet_name="Target", index=False)

    result = data_extractor(str(file_path), sheet_name="Target")

    assert result == [{"b": 2}]


def test_empty_data_error(monkeypatch, tmp_path):
    file_path = tmp_path / "bad.csv"
    file_path.write_text(";;;;", encoding="utf-8")

    def raise_empty(*args, **kwargs):
        raise pd.errors.EmptyDataError("empty")

    monkeypatch.setattr(pd, "read_csv", raise_empty)

    result = data_extractor(str(file_path))
    assert result == []


def test_generic_exception(monkeypatch, tmp_path):
    file_path = tmp_path / "fail.csv"
    file_path.write_text("id;value\n1;100", encoding="utf-8")

    def raise_error(*args, **kwargs):
        raise ValueError("boom")

    monkeypatch.setattr(pd, "read_csv", raise_error)

    result = data_extractor(str(file_path))
    assert result == []