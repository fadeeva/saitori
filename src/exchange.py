from decimal import Decimal
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .order import Order

from src.order import OrderType  
    
from src.orderbook.limit_orderbook import LimitOrderBook
from src.orderbook.stop_orderbook import StopOrderBook

from src.orderlogger import OrderLogger
from src.tradesbook import TradesBook


class Exchange:
    def __init__(self):
        self.tradesbook = TradesBook()
        
        self.limit_orderbook = LimitOrderBook(self.tradesbook)
        self.stop_orderbook = StopOrderBook(self.tradesbook)
        
        self.logger = OrderLogger()
    
    def push(self, order: 'Order') -> None:
        if order.order_type == OrderType.LIMIT:
            self.limit_orderbook.add(order)
        elif order.order_type == OrderType.STOP:
            self.stop_orderbook.add_to_storage(order)
        else:
            pass # MARKET