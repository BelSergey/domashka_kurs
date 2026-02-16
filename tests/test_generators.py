import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


class TestFilterByCurrency:
    """Тесты для функции filter_by_currency."""

    @pytest.mark.parametrize(
        "currency_code, expected_count, expected_ids",
        [
            ("USD", 3, [939719570, 873106923, 895315941]),
            ("RUB", 2, [142264268, 596171168]),
            ("EUR", 0, []),
            ("GBP", 0, []),
        ],
    )
    def test_filter_by_currency(
        self,
        sample_transactions,
        currency_code,
        expected_count,
        expected_ids,
    ):
        """Параметризованный тест фильтрации по валюте."""
        filtered_transactions = list(filter_by_currency(sample_transactions, currency_code))

        assert len(filtered_transactions) == expected_count
        assert [t["id"] for t in filtered_transactions] == expected_ids

        # Проверяем, что у всех отфильтрованных транзакций правильная валюта
        for transaction in filtered_transactions:
            assert transaction["operationAmount"]["currency"]["code"] == currency_code

    def test_filter_by_currency_empty_list(self, empty_transactions):
        """Тест фильтрации пустого списка транзакций."""
        result = list(filter_by_currency(empty_transactions, "USD"))
        assert len(result) == 0

    def test_filter_by_currency_iterator_behavior(self, sample_transactions):
        """Тест поведения итератора."""
        iterator = filter_by_currency(sample_transactions, "USD")

        # Первый вызов next() должен вернуть первую USD транзакцию
        first_transaction = next(iterator)
        assert first_transaction["id"] == 939719570

        # Второй вызов next() должен вернуть вторую USD транзакцию
        second_transaction = next(iterator)
        assert second_transaction["id"] == 873106923

        # После исчерпания итератора должен быть StopIteration
        iterator_exhausted = filter_by_currency(sample_transactions[:1], "EUR")
        with pytest.raises(StopIteration):
            next(iterator_exhausted)


class TestTransactionDescriptions:
    """Тесты для генератора transaction_descriptions."""

    @pytest.mark.parametrize(
        "index, expected_description",
        [
            (0, "Перевод организации"),
            (1, "Перевод со счета на счет"),
            (2, "Перевод со счета на счет"),
            (3, "Перевод с карты на карту"),
            (4, "Открытие вклада"),
        ],
    )
    def test_transaction_descriptions(self, sample_transactions, index, expected_description):
        """Параметризованный тест генератора описаний транзакций."""
        generator = transaction_descriptions(sample_transactions)

        # Пропускаем первые index элементов
        for _ in range(index):
            next(generator)

        # Проверяем index-ый элемент
        description = next(generator)
        assert description == expected_description

    def test_transaction_descriptions_empty_list(self, empty_transactions):
        """Тест генератора с пустым списком транзакций."""
        generator = transaction_descriptions(empty_transactions)

        # Генератор должен сразу завершиться
        with pytest.raises(StopIteration):
            next(generator)

    def test_transaction_descriptions_single(self, single_transaction):
        """Тест генератора с одной транзакцией."""
        generator = transaction_descriptions(single_transaction)

        description = next(generator)
        assert description == "Тестовая транзакция"

        # Должен быть только один элемент
        with pytest.raises(StopIteration):
            next(generator)


class TestCardNumberGenerator:
    """Тесты для генератора card_number_generator."""

    @pytest.mark.parametrize(
        "start, end, expected_results",
        [
            (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
            (
                9999999999999997,
                9999999999999999,
                ["9999 9999 9999 9997", "9999 9999 9999 9998", "9999 9999 9999 9999"],
            ),
            (0, 0, ["0000 0000 0000 0000"]),
            (1234567890123456, 1234567890123456, ["1234 5678 9012 3456"]),
        ],
    )
    def test_card_number_generator_normal_cases(self, start, end, expected_results):
        """Параметризованный тест генератора номеров карт."""
        generator = card_number_generator(start, end)
        results = list(generator)

        assert results == expected_results
        assert len(results) == (end - start + 1)

    @pytest.mark.parametrize(
        "start, end, expected_count",
        [
            (1, 10, 10),
            (100, 199, 100),
            (0, 9999, 10000),
        ],
    )
    def test_card_number_generator_count(self, start, end, expected_count):
        """Тест количества генерируемых номеров карт."""
        generator = card_number_generator(start, end)
        results = list(generator)

        assert len(results) == expected_count

    @pytest.mark.parametrize(
        "start, end",
        [
            (-1, 5),  # Отрицательный start
            (5, -1),  # Отрицательный end
            (10, 5),  # start > end
            (10000000000000000, 10000000000000001),  # Превышение диапазона
        ],
    )
    def test_card_number_generator_invalid_range(self, start, end):
        """Тест генератора с некорректным диапазоном."""
        # Эти значения не должны вызывать ошибку, так как функция не проверяет границы
        # Вместо этого они будут сгенерированы как есть
        generator = card_number_generator(start, end)

        # Для отрицательных чисел форматирование с :016d создаст длинные строки
        # Это технически корректно, но не реалистично
        if start <= end:
            results = list(generator)
            # Просто проверяем, что что-то сгенерировалось
            assert len(results) == (end - start + 1)

    def test_card_number_generator_format(self):
        """Тест формата генерируемых номеров карт."""
        generator = card_number_generator(1, 1)
        card_number = next(generator)

        # Проверяем формат: 4 группы по 4 цифры, разделенные пробелами
        parts = card_number.split(" ")
        assert len(parts) == 4

        for part in parts:
            assert len(part) == 4
            assert part.isdigit()

    def test_card_number_generator_large_range(self):
        """Тест генератора с большим диапазоном."""
        # Тестируем только начало и конец диапазона
        start, end = 123, 456
        generator = card_number_generator(start, end)

        # Проверяем первый элемент
        first = next(generator)
        assert first == "0000 0000 0000 0123"

        # Пропускаем остальные
        for _ in range(end - start):
            next(generator)

        # Проверяем, что итератор завершился
        with pytest.raises(StopIteration):
            next(generator)
