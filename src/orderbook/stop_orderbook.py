from decimal import Decimal
from typing import Literal, List, Optional, Union, Dict, Tuple, Iterator, TYPE_CHECKING
import bisect
from collections import defaultdict

if TYPE_CHECKING:
    from .order import Order
    from src.orderbook.ordersstack import StopOrdersStack

from src.order import OrderSide, OrderTIF
from src.tradesbook import Trade, TradesBook
from src.orderbook.stopordersstack import AskStopOrders, BidStopOrders


class StopOrderBook:
    '''Order book matching bids and asks with price-time priority.'''
    
    def __init__(self):
        self.stop_asks = AskStopOrders()
        self.stop_bids = BidStopOrders()
    
    
    def add(self, order: 'Order') -> None:
        if order.side == OrderSide.ASK:
            opposite_side, same_side = self.stop_bids, self.stop_asks
        else:
            opposite_side, same_side = self.stop_asks, self.stop_bids
        
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
                                same_side: 'StopOrdersStack', opposite_side: 'StopOrdersStack') -> None:
        
        volume = min(incoming.remaining_volume, existing.remaining_volume)
        price = existing.price
        
        incoming.execute(volume=volume, price=price)
        existing.execute(volume=volume, price=price)
        
        self.trades_book.add(
            Trade(incoming, existing, incoming.side, price, volume)
        )
        
        if existing.remaining_volume == 0:
            opposite_side.pop()
            
    
    def clear(self) -> None:
        self.stop_asks.clear()
        self.stop_bids.clear()
    
    @property
    def best_ask(self) -> Optional['Order']:
        return self.stop_asks.peek()
    
    @property
    def best_bid(self) -> Optional['Order']:
        return self.stop_bids.peek()
    
    @property
    def spread(self) -> Decimal:
        return self.best_ask.price - self.best_bid.price
    
    
    def __len__(self):
        return len(self.stop_asks) + len(self.stop_bids)
    
    def __str__(self):
        r = [a.__str__() + ' || ' + b.__str__() + '\n' for a, b in zip(self.stop_asks, self.stop_bids)]
        return ''.join(r)
            
    

    
