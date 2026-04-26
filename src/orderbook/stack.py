from typing import List, Optional, Iterator, TYPE_CHECKING

if TYPE_CHECKING:
    from .order import Order


class Stack:
    ''' Base class for limit and stop orders '''
    
    def __init__(self):
        self._orders: List['Order'] = []
    
    def clear(self) -> None:
        self._orders.clear()
    
    def peek(self) -> Optional['Order']:
        return self._orders[-1] if self._orders else None
    
    def pop(self) -> None:
        self._orders.pop()
    
    def __iter__(self) -> Iterator['Order']:
        return iter(self._orders)
    
    def __reversed__(self):
        for idx in range(len(self._orders)-1, -1, -1):
            yield self._orders[idx]
    
    def __len__(self) -> int:
        return len(self._orders)
    
    def __add__(self, stack: 'Stack') -> List['Orders']:
        return self._orders + stack._orders
    
    def show(self) -> List[dict]:
        return [o.get() for o in self._orders]