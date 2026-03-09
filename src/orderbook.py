from decimal import Decimal
from typing import Literal, List, Optional, Union, Dict, Tuple, Iterator
import bisect
from collections import defaultdict

from src.order import Order, OrderStatus, OrderType, OrderSide, OrderTIF, OrderErrorMessages
from src.tradesbook import Trade, TradesBook


class OrdersStack:
    def __init__(self):
        self._orders: List[Order] = []
    
    def peek(self) -> Optional[Order]:
        return self._orders[-1] if self._orders else None
    
    def pop(self) -> None:
        self._orders.pop()
    
    def show(self) -> List[dict]:
        return [o.get() for o in self._orders]
    
    @property
    def volume(self) -> Decimal:
        return sum(o.volume for o in self._orders)
    
    def get_levels(self, depth: int=5) -> List[Tuple[Decimal, Decimal]]:
        levels = defaultdict(Decimal)
        for o in self._orders:
            levels[o.price] += o.remaining_volume
        
        return list(levels.items())[:depth]
            
    def __iter__(self) -> Iterator[Order]:
        return iter(self._orders)
    
    def __reversed__(self):
        for idx in range(len(self._orders)-1, -1, -1):
            yield self._orders[idx]
    
    def __len__(self) -> int:
        return len(self._orders)
    
#    def __str__(self):
#        r = [o.__repr__() + '\n' for o in self._orders]
#        return ''.join(r)


# from lowest to highest 
class AskOrders(OrdersStack):
    def __init__(self):
        super().__init__()
    
    def push(self, order: Order) -> None:
        idx = bisect.bisect_right([-o.price for o in self._orders], -order.price)
        self._orders.insert(idx, order)
    

# from highest to lowest
class BidOrders(OrdersStack):
    def __init__(self):
        super().__init__()
    
    def push(self, order: Order) -> None:
        idx = bisect.bisect_right([o.price for o in self._orders], order.price)
        self._orders.insert(idx, order)

        
class OrderBook:
    def __init__(self):
        self.asks = AskOrders()
        self.bids = BidOrders()
        self.trades_book = TradesBook()
    
    
    def add(self, order: Order) -> None:
        if order.order_type not in [OrderType.LIMIT, OrderType.STOP]:
            return
        
        if order.side == OrderSide.ASK:
            opposite_side, same_side = self.bids, self.asks
        else:
            opposite_side, same_side = self.asks, self.bids
        
        best_opposite = opposite_side.peek()

        if best_opposite:
            if order.time_in_force is OrderTIF.FOK and not self._is_enough_volume(order, opposite_side):
                return
                
            while order.remaining_volume \
                  and opposite_side.peek() \
                  and self._best_or_equal(order, opposite_side.peek().price):
                self._execute_matched_orders(order, opposite_side.peek(), same_side, opposite_side)
                
        if order.remaining_volume > 0 and order.time_in_force not in [OrderTIF.IOC, OrderTIF.FOK]:
                same_side.push(order)

                
    def _is_enough_volume(self, order: Order, opposite_side: List[Order]) -> bool:
        existing_volume = 0
        for o in reversed(opposite_side):
            if self._best_or_equal(order, o.price):
                existing_volume += o.volume
            else:
                break

        return order.volume <= existing_volume
    
    
    def _best_or_equal(self, order: Order, opposite_price: Decimal) -> bool:
        if order.side == OrderSide.ASK:
            return order.price <= opposite_price
        else:
            return order.price >= opposite_price
    
    
    def _execute_matched_orders(self,
                                incoming: Order, existing: Order,
                                same_side: OrdersStack, opposite_side: OrdersStack) -> None:
        
        volume = min(incoming.remaining_volume, existing.remaining_volume)
        price = existing.price
        
        incoming.execute(volume=volume, price=price)
        existing.execute(volume=volume, price=price)
        
        self.trades_book.add(
            Trade(incoming, existing, incoming.side, price, volume)
        )
        
        if existing.remaining_volume == 0:
            opposite_side.pop()
    
    
    def get_bid_levels(self, depth: int=5) -> List[Tuple[Decimal, Decimal]]:
        return self.bids.get_levels(depth)
    
    def get_ask_levels(self, depth: int=5) -> List[Tuple[Decimal, Decimal]]:
        return self.asks.get_levels(depth)
    
    
    @property
    def best_ask(self) -> Optional[Order]:
        return self.asks.peek()
    
    
    @property
    def best_bid(self) -> Optional[Order]:
        return self.bids.peek()
    
    
    def __len__(self):
        return len(self.asks) + len(self.bids)
    
    
    def __str__(self):
        r = [a.__str__() + ' || ' + b.__str__() + '\n' for a, b in zip(self.asks, self.bids)]
        return ''.join(r)
            
    

    
