from typing import List, Tuple, Optional, TYPE_CHECKING
from decimal import Decimal
import bisect
from collections import defaultdict

if TYPE_CHECKING:
    from .order import Order

from src.orderbook.stack import Stack


class LimitOrdersStack(Stack):
    '''Base class for price-sorted order containers (bids/asks).'''
    
    def __init__(self):
        super().__init__()
    
    def pop(self) -> None:
        self._orders.pop()
    
    def push(self, order: 'Order') -> None:
        raise NotImplementedError('Subclasses must implement push()')
    
    @property
    def volume(self) -> Decimal:
        return sum(o.volume for o in self._orders)
    
    def get_levels(self, depth: int=5) -> List[Tuple[Decimal, Decimal]]:
        levels = defaultdict(Decimal)
        for o in self._orders:
            levels[o.price] += o.remaining_volume
        
        return list(levels.items())[:depth]


class AskOrders(LimitOrdersStack):
    '''Ask orders sorted from lowest to highest price.'''
    
    def __init__(self):
        super().__init__()
    
    def push(self, order: 'Order') -> None:
        idx = bisect.bisect_right([-o.price for o in self._orders], -order.price)
        self._orders.insert(idx, order)
    

class BidOrders(LimitOrdersStack):
    '''Bid orders sorted from highest to lowest price.'''
    
    def __init__(self):
        super().__init__()
    
    def push(self, order: 'Order') -> None:
        idx = bisect.bisect_right([o.price for o in self._orders], order.price)
        self._orders.insert(idx, order)

