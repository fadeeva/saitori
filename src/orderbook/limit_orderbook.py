from decimal import Decimal
from typing import Literal, List, Optional, Union, Dict, Tuple, Iterator, TYPE_CHECKING
import bisect
from collections import defaultdict

if TYPE_CHECKING:
    from .order import Order
    from src.orderbook.limit_orders_stack import OrdersStack

from src.order import OrderSide, OrderTIF
from src.orderbook.limit_orders_stack import AskOrders, BidOrders

from src.orderbook.matching_engine import MatchingEngine


class LimitOrderBook:
    '''Order book matching bids and asks with price-time priority.'''
    
    def __init__(self):        
        self.me = MatchingEngine(AskOrders(), BidOrders())
    
    def add(self, order: 'Order') -> None:
        self.me.add(order)
    
    def get_bid_levels(self, depth: int=5) -> List[Tuple[Decimal, Decimal]]:
        return self.me.bids.get_levels(depth)
    
    def get_ask_levels(self, depth: int=5) -> List[Tuple[Decimal, Decimal]]:
        return self.me.asks.get_levels(depth)
    
    def clear(self) -> None:
        self.me.clear()
    
    @property
    def best_ask(self) -> Optional['Order']:
        return self.me.asks.peek()
    
    @property
    def best_bid(self) -> Optional['Order']:
        return self.me.bids.peek()
    
    @property
    def spread(self) -> Optional[Decimal]:
        if self.best_ask and self.best_bid:
            return self.best_ask.price - self.best_bid.price
        return None
        
    def __len__(self):
        return len(self.me.asks) + len(self.me.bids)
    
    def __str__(self):
        r = [a.__str__() + ' || ' + b.__str__() + '\n' for a, b in zip(self.me.asks, self.me.bids)]
        return ''.join(r)
            
    

    
