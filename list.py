from typing import List, Optional, TypeVar

T = TypeVar('T')
def pick_first(lst: List[T]) -> Optional[T]:
    return lst[0] if len(lst) > 0 else None