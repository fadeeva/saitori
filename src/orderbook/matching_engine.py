from decimal import Decimal
from typing import Literal, List, Optional, Union, Dict, Tuple, Iterator, TYPE_CHECKING
import bisect
from collections import defaultdict

if TYPE_CHECKING:
    from src.order import Order
    from src.orderbook.stop_orders_stack import StopOrdersStack, AskStopOrders, BidStopOrders
    from src.orderbook.limit_orders_stack import OrdersStack, AskOrders, BidOrders

from src.order import OrderSide, OrderTIF
from src.tradesbook import Trade


class MatchingEngine:
    
    def __init__(self,
                 asks: Union['AskOrders', 'AskStopOrders'],
                 bids: Union['BidOrders', 'BidStopOrders']):
        self.asks = asks
        self.bids = bids
    
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
                self._execute_matched_orders(order, opposite_side.peek(), opposite_side)
                
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
                                opposite_side: 'OrdersStack') -> Optional[Trade]:
        
        volume = min(incoming.remaining_volume, existing.remaining_volume)
        price = existing.price
        
        incoming.execute(volume=volume, price=price)
        existing.execute(volume=volume, price=price)
        
        if existing.remaining_volume == 0:
            opposite_side.pop()
        
        return Trade(incoming, existing, incoming.side, price, volume)
            
    def clear(self) -> None:
        self.asks.clear()
        self.bids.clear()
