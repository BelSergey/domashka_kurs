import re
from typing import List, Dict, Any

def filter_by_description(data: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """Фильтрует список банковских операций. """
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    result = []
    for record in data:
        description = record.get('description')
        if not isinstance(description, str):
            description = str(description) if description is not None else ''
        if pattern.search(description):
            result.append(record)
    return result





