def filter_by_state(operations, state='EXECUTED'):
    """ Фильтрует список словарей по значению ключа 'state'"""
    filtered_operations = []
    for operation in operations:
        if operation.get('state') == state:
            filtered_operations.append(operation)
    return filtered_operations


def sort_by_date(operations, reverse=True):
    """ Сортирует список словарей по дате """
    sorted_operations = operations.copy()
    sorted_operations.sort(key=lambda x: x.get('date', ''), reverse=reverse)

    return sorted_operations

