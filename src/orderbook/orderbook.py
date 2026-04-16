from decimal import Decimal
from typing import Union, List, TYPE_CHECKING

from itertools import zip_longest

if TYPE_CHECKING:
    from src.order import Order
    from src.tradesbook import TradesBook
    from src.orderbook.stop_orders_stack import AskStopOrders, BidStopOrders
    from src.orderbook.limit_orders_stack import AskOrders, BidOrders
    
from src.orderbook.matching_engine import MatchingEngine


class OrderBook:
    '''Order book base class for limit and stop orders.'''
    
    def __init__(self,
                 asks: Union['AskOrders', 'AskStopOrders'],
                 bids: Union['BidOrders', 'BidStopOrders'],
                 tradesbook: 'TradesBook'):
        
        self.me = MatchingEngine(asks, bids, tradesbook)
    
    def add(self, order: 'Order'):
        self.me.add(order)
    
    def clear(self) -> None:
        self.me.clear()
    
    @property
    def asks(self) -> List['Orders']:
        return self.me.asks
    
    @property
    def bids(self) -> List['Orders']:
        return self.me.bids
    
    def cancel(self, order: 'Order') -> None:
        pass
    
    def __len__(self):
        return len(self.asks) + len(self.bids)
    
    def __str__(self):
        r = [str(a) + ' || ' + str(b) + '\n' for a, b in zip_longest(self.asks, self.bids)]
        return ''.join(r)
            
    

    
