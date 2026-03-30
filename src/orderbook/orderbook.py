from decimal import Decimal
from typing import Literal, List, Optional, Union, Dict, Tuple, Iterator, TYPE_CHECKING
import bisect
from collections import defaultdict

if TYPE_CHECKING:
    from .order import Order
    from src.orderbook.ordersstack import OrdersStack

from src.order import OrderType, OrderSide, OrderTIF
from src.tradesbook import Trade, TradesBook
from src.orderbook.ordersstack import AskOrders, BidOrders
from src.orderbook.stopordersstack import AskStopOrders, BidStopOrders


class OrderBook:
    '''Order book matching bids and asks with price-time priority.'''
    
    def __init__(self):
        self.asks = AskOrders()
        self.bids = BidOrders()
        
        self.stop_asks = AskStopOrders()
        self.stop_bids = BidStopOrders()
        
        self.trades_book = TradesBook()
        
        self.last_trade_price: Optional[Decimal] = None
    
    
    def add(self, order: 'Order') -> None:
        if order.order_type == OrderType.STOP:
            self._add_stop_order(order)
            return
        
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
        if order.order_type == OrderType.MARKET: return True
        
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
        
        self.last_trade_price = price
        self._check_stop_orders()
        
        self.trades_book.add(
            Trade(incoming, existing, incoming.side, price, volume)
        )
        
        if existing.remaining_volume == 0:
            opposite_side.pop()
    
    def _add_stop_order(self, order: 'Order'):
        if order.side == OrderSide.ASK:
            self.stop_asks.push(order)
        else:
            self.stop_bids.push(order)
    
    
    def _check_stop_orders(self):
        pass
    
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
    def spread(self) -> Decimal:
        return self.best_ask.price - self.best_bid.price
    
    
    def __len__(self):
        return len(self.asks) + len(self.bids)
    
    
    def __str__(self):
        r = [a.__str__() + ' || ' + b.__str__() + '\n' for a, b in zip(self.asks, self.bids)]
        return ''.join(r)
            
    

    
