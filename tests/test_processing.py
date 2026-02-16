import pytest

from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    """Тесты для фильтрации операций по состоянию"""

    def test_filter_by_state_from_fixture(self, sample_operations, state_and_expected_ids):
        """Тест фильтрации по состоянию из фикстуры"""
        state, expected_ids = state_and_expected_ids
        result = filter_by_state(sample_operations, state)
        assert [op["id"] for op in result] == expected_ids

    def test_filter_default_state(self, sample_operations):
        """Тест фильтрации с состоянием по умолчанию"""
        result = filter_by_state(sample_operations)
        assert len(result) == 3
        assert all(op["state"] == "EXECUTED" for op in result)

    def test_filter_empty_list(self):
        """Тест фильтрации пустого списка"""
        result = filter_by_state([], "EXECUTED")
        assert result == []

    @pytest.mark.parametrize(
        "state, expected_count",
        [
            ("EXECUTED", 3),
            ("CANCELED", 1),
            ("PENDING", 1),
            ("NONEXISTENT", 0),
        ],
    )
    def test_filter_counts_parametrized(self, sample_operations, state, expected_count):
        """Параметризованный тест количества отфильтрованных операций"""
        result = filter_by_state(sample_operations, state)
        assert len(result) == expected_count

    def test_filter_returns_new_list(self, sample_operations):
        """Тест, что функция возвращает новый список"""
        result = filter_by_state(sample_operations, "EXECUTED")
        assert result is not sample_operations
        result.append({"id": 999, "state": "EXECUTED"})
        assert len(sample_operations) == 8

    def test_filter_large_dataset(self):
        """Тест фильтрации большого набора данных"""
        operations = [{"id": i, "state": "EXECUTED" if i % 2 == 0 else "CANCELED"} for i in range(1000)]
        result = filter_by_state(operations, "EXECUTED")
        assert len(result) == 500
        assert all(op["state"] == "EXECUTED" for op in result)


class TestSortByDate:
    """Тесты для сортировки операций по дате"""

    def test_sort_by_date_from_fixture(self, operations_for_sorting, reverse_and_first_id):
        """Тест сортировки из фикстуры"""
        reverse, expected_first_id = reverse_and_first_id
        result = sort_by_date(operations_for_sorting, reverse=reverse)

        # Находим первый элемент с датой
        first_with_date = next((op for op in result if "date" in op), None)
        if first_with_date:
            assert first_with_date["id"] == expected_first_id

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

    @pytest.mark.parametrize(
        "reverse, expected_order",
        [
            (True, [2, 3, 6, 7, 1, 4]),  # По убыванию
            (False, [4, 1, 7, 6, 3, 2]),  # По возрастанию
        ],
    )
    def test_sort_order_parametrized(self, operations_for_sorting, reverse, expected_order):
        """Параметризованный тест порядка сортировки"""
        result = sort_by_date(operations_for_sorting, reverse=reverse)
        # Фильтруем только операции с датами
        ids_with_date = [op["id"] for op in result if "date" in op]
        assert ids_with_date == expected_order

    def test_sort_returns_new_list(self, operations_for_sorting):
        """Тест, что функция возвращает новый список"""
        result = sort_by_date(operations_for_sorting)
        assert result is not operations_for_sorting
        result.append({"id": 999, "date": "2023-01-01"})
        assert len(operations_for_sorting) == 7

    @pytest.mark.parametrize(
        "operations, expected_ids",
        [
            ([{"id": 1, "date": "2023-01-01"}, {"id": 2, "date": "2023-01-02"}], [2, 1]),
            ([{"id": 1, "date": "2022-12-31"}, {"id": 2, "date": "2023-01-01"}], [2, 1]),
        ],
    )
    def test_specific_sorting_cases_parametrized(self, operations, expected_ids):
        """Параметризованные тесты конкретных случаев сортировки"""
        result = sort_by_date(operations, reverse=True)
        assert [op["id"] for op in result] == expected_ids
