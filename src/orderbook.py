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
        idx = bisect.bisect_right([o.price for o in self._orders], order.price)
        self._orders.insert(idx, order)
    

# from highest to lowest
class BidOrders(OrdersStack):
    def __init__(self):
        super().__init__()
    
    def push(self, order: Order) -> None:
        idx = bisect.bisect_right([-o.price for o in self._orders], -order.price)
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
            best_opposite = self.best_bid
        else:
            opposite_side, same_side = self.asks, self.bids
            best_opposite = self.best_ask
        
        if best_opposite and self._best_or_equal(order.price, best_opposite.price, order.side):
            self._execute_matched_orders(order, best_opposite, same_side, opposite_side)
        else:
            same_side.push(order)
            
#        if best_opposite:
#            while _best_or_equal(order.price, opposite_side.peek().price, order.side):
#                pass
#        else:
#            same_side.push(order)
    
    def _best_or_equal(self,
                       price: Decimal, opposite_price: Decimal,
                       side: OrderSide) -> bool:
        if side == OrderSide.ASK:
            return price <= opposite_price
        else:
            return price >= opposite_price
    
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
            
        if incoming.remaining_volume > 0:
            same_side.push(incoming)
    
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
    

    
