from typing import Any, Dict, List
import re
from collections import Counter


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """ Фильтрует список словарей по значению ключа 'state' . """
    state_upper = state.upper()
    filtered = []
    for op in operations:
        if op.get("state", "").upper() == state_upper:
            filtered.append(op)
    return filtered


def sort_by_date(operations: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Сортирует список словарей по дате"""
    sorted_operations: List[Dict[str, Any]] = operations.copy()
    sorted_operations.sort(key=lambda x: x.get("date", ""), reverse=reverse)

    return sorted_operations

def filter_by_description(data: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """ Фильтрует операции по вхождению строки в поле 'description'. """
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    result = []
    for record in data:
        description = record.get('description')
        if not isinstance(description, str):
            description = str(description) if description is not None else ''
        if pattern.search(description):
            result.append(record)
    return result

def count_operations_by_categories(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """ Подсчитывает количество операций в каждой категории. """
    descriptions_lower = []
    for item in data:
        if 'description' in item:
            desc = item['description']
            if not isinstance(desc, str):

                if isinstance(desc, float) and desc.is_integer():
                    desc = str(int(desc))
                else:
                    desc = str(desc) if desc is not None else ''
            descriptions_lower.append(desc.lower())

    counter_lower = Counter(descriptions_lower)

    result = {}
    for category in categories:
        result[category] = counter_lower.get(category.lower(), 0)
    return result
