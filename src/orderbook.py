from typing import Literal, List, Optional, Union, Dict, Tuple
import bisect

from src.order import Order, OrderStatus, OrderType, OrderSide, OrderTIF, OrderErrorMessages

class OrdersStack:
    def __init__(self):
        self._orders: List[Order] = []
    
    def peek(self) -> Optional[Order]:
        return self._orders[-1] if self._orders else None
    
    def remove(self) -> None:
        self._orders.pop()
    
    def __len__(self) -> int:
        return len(self._orders)
    
    def show(self) -> List[dict]:
        return [o.get() for o in self._orders]


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
        if order.side == OrderSide.ASK:
            if not len(self.bids):
                self.asks.push(order)
            elif order.price == self.best_bid.price:
                if order.volume > self.best_bid.volume:
                    order.execute(volume=self.best_bid.volume, price=self.best_bid.price)
                    self.best_bid.execute(volume=self.best_bid.volume, price=self.best_bid.price)
                    self.bids.remove()
                    # note in Trade
                    self.asks.push(order)
                else:
                    order.execute(volume=order.volume, price=self.best_bid.price)
                    self.best_bid.execute(volume=order.volume, price=self.best_bid.price)
                    # note in Trade
                    
        else:
            if not len(self.asks):
                self.bids.push(order)
            elif order.price == self.best_ask.price:
                if order.volume > self.best_ask.volume:
                    order.execute(volume=self.best_ask.volume, price=self.best_ask.price)
                    self.best_ask.execute(volume=self.best_ask.volume, price=self.best_ask.price)
                    self.asks.remove()
                    # note in Trade
                    self.bids.push(order)
                else:
                    order.execute(volume=order.volume, price=self.best_ask.price)
                    self.best_ask.execute(volume=order.volume, price=self.best_ask.price)
                    # note in Trade
    
    def execute(self) -> None:
        pass
    
    @property
    def best_ask(self) -> Optional[Order]:
        return self.asks.peek()
    
    @property
    def best_bid(self) -> Optional[Order]:
        return self.bids.peek()
    
    
    def __str__(self) -> str:
        return str(self.asks.show()) + str(self.bids.show())
    

    
