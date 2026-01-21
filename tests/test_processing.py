import pytest
from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    """Тесты для фильтрации операций по состоянию"""

    @pytest.fixture
    def sample_operations(self):
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
    def empty_operations(self):
        """Фикстура с пустым списком операций"""
        return []

    @pytest.fixture
    def operations_without_state(self):
        """Фикстура с операциями без ключа state"""
        return [
            {"id": 1, "date": "2023-01-01"},
            {"id": 2, "date": "2023-01-02"},
            {"id": 3, "date": "2023-01-03"},
        ]

    @pytest.mark.parametrize("state, expected_ids", [
        ("EXECUTED", [1, 3, 5]),
        ("CANCELED", [2]),
        ("PENDING", [4]),
        ("NONEXISTENT", []),
        ("executed", []),  # Регистр имеет значение
        ("", []),  # Пустая строка
    ])
    def test_filter_by_state_parametrized(self, sample_operations, state, expected_ids):
        """Параметризованный тест фильтрации по разным состояниям"""
        result = filter_by_state(sample_operations, state)
        assert [op["id"] for op in result] == expected_ids

    def test_filter_default_state(self, sample_operations):
        """Тест фильтрации с состоянием по умолчанию"""
        result = filter_by_state(sample_operations)
        assert len(result) == 3
        assert all(op["state"] == "EXECUTED" for op in result)

    def test_filter_empty_list(self, empty_operations):
        """Тест фильтрации пустого списка"""
        result = filter_by_state(empty_operations, "EXECUTED")
        assert result == []

    def test_filter_operations_without_state(self, operations_without_state):
        """Тест фильтрации операций без ключа state"""
        result = filter_by_state(operations_without_state, "EXECUTED")
        assert result == []

    def test_filter_with_state_none(self, sample_operations):
        """Тест фильтрации с state = None"""
        result = filter_by_state(sample_operations, None)
        assert [op["id"] for op in result] == [7]

    def test_filter_large_dataset(self):
        """Тест фильтрации большого набора данных"""
        operations = []
        for i in range(1000):
            state = "EXECUTED" if i % 2 == 0 else "CANCELED"
            operations.append({"id": i, "state": state, "date": "2023-01-01"})

        result = filter_by_state(operations, "EXECUTED")
        assert len(result) == 500
        assert all(op["state"] == "EXECUTED" for op in result)

    def test_filter_returns_new_list(self, sample_operations):
        """Тест, что функция возвращает новый список"""
        result = filter_by_state(sample_operations, "EXECUTED")
        assert result is not sample_operations
        result.append({"id": 999, "state": "EXECUTED"})
        assert len(sample_operations) == 8


class TestSortByDate:
    """Тесты для сортировки операций по дате"""

    @pytest.fixture
    def sample_operations(self):
        """Фикстура с примером операций для сортировки"""
        return [
            {"id": 1, "date": "2023-01-01", "amount": 100},
            {"id": 2, "date": "2023-01-03", "amount": 200},
            {"id": 3, "date": "2023-01-02", "amount": 300},
            {"id": 4, "date": "2022-12-31", "amount": 400},
            {"id": 5, "amount": 500},  # Нет даты
            {"id": 6, "date": "2023-01-01T12:00:00", "amount": 600},
            {"id": 7, "date": "2023-01-01T08:00:00", "amount": 700},
        ]

    @pytest.fixture
    def operations_with_same_date(self):
        """Фикстура с операциями с одинаковыми датами"""
        return [
            {"id": 1, "date": "2023-01-01"},
            {"id": 2, "date": "2023-01-01"},
            {"id": 3, "date": "2023-01-01"},
            {"id": 4, "date": "2023-01-02"},
            {"id": 5, "date": "2023-01-02"},
        ]

    @pytest.fixture
    def operations_without_dates(self):
        """Фикстура с операциями без дат"""
        return [
            {"id": 1, "amount": 100},
            {"id": 2, "amount": 200},
            {"id": 3, "amount": 300},
        ]

    def test_sort_descending_default(self, sample_operations):
        """Тест сортировки по убыванию (по умолчанию)"""
        result = sort_by_date(sample_operations)

        ids = [op["id"] for op in result if "date" in op]
        assert ids == [2, 3, 6, 7, 1, 4]
        assert result[-1]["id"] == 5

    def test_sort_descending_explicit(self, sample_operations):
        """Тест сортировки по убыванию (явно)"""
        result = sort_by_date(sample_operations, reverse=True)
        ids = [op["id"] for op in result if "date" in op]
        assert ids == [2, 3, 6, 7, 1, 4]

    def test_sort_ascending(self, sample_operations):
        """Тест сортировки по возрастанию"""
        result = sort_by_date(sample_operations, reverse=False)
        assert result[0]["id"] == 5

        # Проверяем порядок остальных
        ids = [op["id"] for op in result[1:]]
        assert ids == [4, 1, 7, 6, 3, 2]

    def test_sort_empty_list(self):
        """Тест сортировки пустого списка"""
        result = sort_by_date([])
        assert result == []

    def test_sort_single_element(self):
        """Тест сортировки списка с одним элементом"""
        operations = [{"id": 1, "date": "2023-01-01"}]
        result = sort_by_date(operations)
        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_sort_returns_new_list(self, sample_operations):
        """Тест, что функция возвращает новый список"""
        result = sort_by_date(sample_operations)
        assert result is not sample_operations
        result.append({"id": 999, "date": "2023-01-01"})
        assert len(sample_operations) == 7

    def test_sort_with_same_dates(self, operations_with_same_date):
        """Тест сортировки с одинаковыми датами"""
        result = sort_by_date(operations_with_same_date, reverse=True)
        ids = [op["id"] for op in result]
        assert ids == [4, 5, 1, 2, 3]

    def test_sort_without_dates(self, operations_without_dates):
        """Тест сортировки операций без дат"""
        result = sort_by_date(operations_without_dates)
        assert [op["id"] for op in result] == [1, 2, 3]

    @pytest.mark.parametrize("reverse, expected_first_id", [
        (True, 2),
        (False, 4),
    ])
    def test_sort_parametrized(self, sample_operations, reverse, expected_first_id):
        """Параметризованный тест сортировки"""
        result = sort_by_date(sample_operations, reverse=reverse)
        first_with_date = next((op for op in result if "date" in op), None)
        if first_with_date:
            assert first_with_date["id"] == expected_first_id

    def test_sort_with_invalid_date_format(self):
        """Тест сортировки с некорректным форматом даты"""
        operations = [
            {"id": 1, "date": "2023-01-01"},
            {"id": 2, "date": "invalid-date"},
            {"id": 3, "date": "2023-01-02"},
        ]
        result = sort_by_date(operations, reverse=True)
        assert [op["id"] for op in result] == [3, 1, 2]