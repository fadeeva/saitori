from decimal import Decimal
from typing import List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .order import Order

from src.orderbook.limit_orders_stack import AskOrders, BidOrders
from src.orderbook.orderbook import OrderBook


class LimitOrderBook(OrderBook):
    '''Order book matching bids and asks with price-time priority for limit orders.'''
    
    def __init__(self):
        super().__init__(AskOrders(), BidOrders())
    
    def get_bid_levels(self, depth: int=5) -> List[Tuple[Decimal, Decimal]]:
        return self.bids.get_levels(depth)
    
    def get_ask_levels(self, depth: int=5) -> List[Tuple[Decimal, Decimal]]:
        return self.asks.get_levels(depth)
    
    @property
    def best_ask(self) -> Optional['Order']:
        return self.asks.peek()
    
    @property
    def best_bid(self) -> Optional['Order']:
        return self.bids.peek()
    
    @property
    def spread(self) -> Optional[Decimal]:
        if self.best_ask and self.best_bid:
            return self.best_ask.price - self.best_bid.price
        return None
            
    

    
