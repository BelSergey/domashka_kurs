from typing import List, Dict, Any


def filter_by_state(operations: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """ Фильтрует список словарей по значению ключа 'state' """
    filtered_operations: List[Dict[str, Any]] = []
    for operation in operations:
        if operation.get('state') == state:
            filtered_operations.append(operation)
    return filtered_operations


def sort_by_date(operations: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """ Сортирует список словарей по дате """
    sorted_operations: List[Dict[str, Any]] = operations.copy()
    sorted_operations.sort(key=lambda x: x.get('date', ''), reverse=reverse)

    return sorted_operations