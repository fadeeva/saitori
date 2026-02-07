from typing import Literal, List, Optional, Union, Dict, Tuple
import bisect

from src.order import Order, OrderStatus, OrderType, OrderSide, OrderTIF, OrderErrorMessages

class OrdersStack:
    def __init__(self):
        self._orders: List[Order] = []
    
    def peek(self)->Optional[Order]:
        return self._orders[-1] if self._orders else None
    
    def show(self)->List[dict]:
        return [o.get() for o in self._orders]


# from lowest to highest 
class AskOrders(OrdersStack):
    def __init__(self):
        super().__init__()
    
    def push(self, order:Order)->None:
        idx = bisect.bisect_right([o.price for o in self._orders], order.price)
        self._orders.insert(idx, order)
    

# from highest to lowest
class BidOrders(OrdersStack):
    def __init__(self):
        super().__init__()
    
    def push(self, order:Order)->None:
        idx = bisect.bisect_right([-o.price for o in self._orders], -order.price)
        self._orders.insert(idx, order)

        
class OrderBook:
    def __init__(self):
        self.asks = AskOrders()
        self.bids = BidOrders()
    
    def add(self, order:Order)->None:
        if order.side == OrderSide.ASK:
            self.asks.push(order)
        else:
            self.bids.push(order)
    
    @property
    def best_ask(self)->Optional[Order]:
        return self.asks.peek()
    
    @property
    def best_bid(self)->Optional[Order]:
        return self.bids.peek()
    
    def __str__(self) -> str:
        return str(self.asks.show()) + str(self.bids.show())
    

    
