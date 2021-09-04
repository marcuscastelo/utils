from typing import List, TypeVar

T = TypeVar('T')
def pick_first(lst: List[T]) -> T:
    return lst[0] if len(lst) > 0 else None