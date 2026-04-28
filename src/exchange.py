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
        
        self.limit_orderbook = LimitOrderBook()
        self.stop_orderbook = StopOrderBook()
        
        self.logger = OrderLogger()
    
    def push(self, order: 'Order') -> None:
        trades = []
        if order.order_type in [OrderType.LIMIT, OrderType.MARKET]:
            trades = self.limit_orderbook.add(order, exchange=self)
        elif order.order_type == OrderType.STOP:
            self.stop_orderbook.add_to_storage(order)
        
        if trades:
            for trade in trades:
                self.tradesbook.add(trade)
                
    def check_stop_orders(self, trade):
        orders = self.stop_orderbook.get_activated(trade.price)
        if orders:
            for o in orders:
                self.push(o)
                
    def status(self):
        return True