from decimal import Decimal
from typing import Literal, List, Optional, Union, Dict, Tuple, Iterator, TYPE_CHECKING
import bisect
from collections import defaultdict

if TYPE_CHECKING:
    from .order import Order
    from src.orderbook.limit_orders_stack import OrdersStack

from src.order import OrderSide, OrderTIF
from src.orderbook.limit_orders_stack import AskOrders, BidOrders


class OrderBook:
    '''Order book matching bids and asks with price-time priority.'''
    
    def __init__(self):
        self.asks = AskOrders()
        self.bids = BidOrders()
    
    def add(self, order: 'Order') -> None:
        if order.side == OrderSide.ASK:
            opposite_side, same_side = self.bids, self.asks
        else:
            opposite_side, same_side = self.asks, self.bids
        
        best_opposite = opposite_side.peek()

        if best_opposite:
            if order.time_in_force is OrderTIF.FOK and not self._is_enough_volume(order, opposite_side):
                order.cancel()
                return
                
            while order.remaining_volume \
                  and opposite_side.peek() \
                  and self._best_or_equal(order, opposite_side.peek().price):
                self._execute_matched_orders(order, opposite_side.peek(), same_side, opposite_side)
                
        if order.remaining_volume > 0 and order.time_in_force not in [OrderTIF.IOC, OrderTIF.FOK]:
            same_side.push(order)

                
    def _is_enough_volume(self, order: 'Order', opposite_side: List['Order']) -> bool:
        existing_volume = 0
        for o in reversed(opposite_side):
            if self._best_or_equal(order, o.price):
                existing_volume += o.volume
            else:
                break

        return order.volume <= existing_volume
    
    
    def _best_or_equal(self, order: 'Order', opposite_price: Decimal) -> bool:
        if order.side == OrderSide.ASK:
            return order.price <= opposite_price
        else:
            return order.price >= opposite_price
    
    
    def _execute_matched_orders(self,
                                incoming: 'Order', existing: 'Order',
                                same_side: 'OrdersStack', opposite_side: 'OrdersStack') -> None:
        
        volume = min(incoming.remaining_volume, existing.remaining_volume)
        price = existing.price
        
        incoming.execute(volume=volume, price=price)
        existing.execute(volume=volume, price=price)
        
        if existing.remaining_volume == 0:
            opposite_side.pop()
        
    
    def get_bid_levels(self, depth: int=5) -> List[Tuple[Decimal, Decimal]]:
        return self.bids.get_levels(depth)
    
    def get_ask_levels(self, depth: int=5) -> List[Tuple[Decimal, Decimal]]:
        return self.asks.get_levels(depth)
    
    def clear(self) -> None:
        self.asks.clear()
        self.bids.clear()
    
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
        
    
    
    def __len__(self):
        return len(self.asks) + len(self.bids)
    
    def __str__(self):
        r = [a.__str__() + ' || ' + b.__str__() + '\n' for a, b in zip(self.asks, self.bids)]
        return ''.join(r)
            
    

    
