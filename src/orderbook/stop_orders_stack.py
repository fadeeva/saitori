from typing import List, Tuple, Optional, TYPE_CHECKING
from decimal import Decimal
import bisect
from collections import defaultdict

if TYPE_CHECKING:
    from .order import Order

from src.orderbook.stack import Stack
from src.order import OrderType


class StopOrdersStack(Stack):
    '''Base class for stop orders.'''
    
    def __init__(self):
        super().__init__()
    
    def push(self, order: 'Order') -> None:
        raise NotImplementedError('Subclasses must implement push()')
    
    def get_activated(self, current_price: Decimal) -> List['Order']:
        raise NotImplementedError('Subclasses must implement get_activated()')
        

class AskStopOrders(StopOrdersStack):
    '''Ask stop orders (sorted?) from lowest to highest price.'''
    
    def __init__(self):
        super().__init__()
    
    def get_activated(self, current_price: Decimal) -> List['Order']:
        activated = []
        for o in self._orders[:]:
            if current_price <= o.stop_price:
                o.order_type = OrderType.LIMIT if o.price else OrderType.MARKET
                activated.append(o)
                self._orders.remove(o)
        return activated
    
    def push(self, order: 'Order') -> None:
        idx = bisect.bisect_right([-o.stop_price for o in self._orders], -order.stop_price)
        self._orders.insert(idx, order)


class BidStopOrders(StopOrdersStack):
    '''Bid stop orders (sorted?) from highest to lowest price.'''
    
    def __init__(self):
        super().__init__()
        
    def get_activated(self, current_price: Decimal) -> List['Order']:
        activated = []
        for o in self._orders[:]:
            if current_price >= o.stop_price:
                o.order_type = OrderType.LIMIT if o.price else OrderType.MARKET
                activated.append(o)
                self._orders.remove(o)
                
        return activated
    
    def push(self, order: 'Order') -> None:
        idx = bisect.bisect_right([o.stop_price for o in self._orders], order.stop_price)
        self._orders.insert(idx, order)
    
    