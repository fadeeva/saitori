from decimal import Decimal
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .order import Order

from src.order import OrderSide 
from src.orderbook.stop_orders_stack import AskStopOrders, BidStopOrders
from src.orderbook.orderbook import OrderBook


class StopOrderBook(OrderBook):
    '''Order book matching bids and asks with price-time priority for stop orders.'''
    
    def __init__(self):
        super().__init__(AskStopOrders(), BidStopOrders())
        
        self._ask_storage = AskStopOrders()
        self._bid_storage = BidStopOrders()
    
    def add_to_storage(self, order: 'Order') -> None:
        if order.side == OrderSide.ASK:
            self._ask_storage.push(order)
        else:
            self._bid_storage.push(order)
    
    def get_activated(self, current_price: Decimal) -> Optional[List['Order']]:
        activated_asks = self._ask_storage.get_activated(current_price)
        activated_bids = self._bid_storage.get_activated(current_price)
        
        activated_orders = activated_asks + activated_bids
        activated_orders.sort(key=lambda o: o.timestamp)
        
        for o in activated_orders:
            self.add(o)
        
        unexecuted_orders = self.asks + self.bids
        
        if unexecuted_orders:
            self.clear()
            return unexecuted_orders.sort(key=lambda o: o.timestamp)
    
    @property
    def storage_len(self) -> int:
        return len(self._ask_storage) + len(self._bid_storage)
    
    @property
    def ask_storage(self) -> List['Orders']:
        return self._ask_storage
    
    @property
    def bid_storage(self) -> List['Orders']:
        return self._bid_storage
        
            
            
    
