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
        self.ask_storage = AskStopOrders()
        self.bid_storage = BidStopOrders()
    
    def add_to_storage(self, order: 'Order') -> None:
        if order.side == OrderSide.ASK:
            self.ask_storage.push(order)
        else:
            self.bid_storage.push(order)
    
    def get_activated(self, current_price: Decimal) -> Optional[List['Order']]:
        activated_asks = self.ask_storage.get_activated(current_price)
        activated_bids = self.bid_storage.get_activated(current_price)
        
        # unite, sort by timestamp, add order by order to self.add()
            
    
