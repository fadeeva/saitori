from decimal import Decimal
from typing import Literal, List, Optional, Union, Dict, Tuple
import bisect

from src.order import Order, OrderStatus, OrderType, OrderSide, OrderTIF, OrderErrorMessages


class OrdersStack:
    def __init__(self):
        self._orders: List[Order] = []
    
    def peek(self) -> Optional[Order]:
        return self._orders[-1] if self._orders else None
    
    def pop(self) -> None:
        self._orders.pop()
    
    def show(self) -> List[dict]:
        return [o.get() for o in self._orders]
    
    def __len__(self) -> int:
        return len(self._orders)
    
    def __str__(self):
        return f'{self.__dict__}'


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
    
    def add(self, order: Order) -> None:
        if order.order_type not in [OrderType.LIMIT, OrderType.STOP]:
            return
        
        if order.side == OrderSide.ASK:
            opposite_side, same_side = self.bids, self.asks
        else:
            opposite_side, same_side = self.asks, self.bids
        
        best_opposite = opposite_side.peek()
        if best_opposite:
            while order.remaining_volume and self._best_or_equal(order, opposite_side.peek().price):
                self._execute_matched_orders(order, opposite_side.peek(), same_side, opposite_side)
            
            if order.remaining_volume > 0:
                same_side.push(order)
        else:
            same_side.push(order)
    
    def _best_or_equal(self, order: Order, opposite_price: Decimal) -> bool:
        if order.side == OrderSide.ASK:
            return order.price <= opposite_price
        else:
            return order.price >= opposite_price
    
    def _execute_matched_orders(self,
                                incoming: Order, existing: Order,
                                same_side: OrdersStack, opposite_side: OrdersStack) -> None:
        volume = min(incoming.volume, existing.volume)
        price = existing.price
        
        incoming.execute(volume=volume, price=price)
        existing.execute(volume=volume, price=price)
        # add note about trade to Trade
        
        if existing.remaining_volume == 0:
            opposite_side.pop()
    
    @property
    def best_ask(self) -> Optional[Order]:
        return self.asks.peek()
    
    @property
    def best_bid(self) -> Optional[Order]:
        return self.bids.peek()
    
    def __len__(self):
        return len(self.asks) + len(self.bids)
    
    def __str__(self):
        return f'{str(self.asks)}, {str(self.bids)}'
    

    
