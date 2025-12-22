from typing import Literal, List, Optional
from datetime import datetime
import bisect


class Order:
    def __init__(self,
                 side:Literal['bid', 'ask'],
                 price:float, volume:int):
        self.side = side
        self.volume = volume
        self.price = price
        self.timestamp = datetime.now()
        self.id = id(self)
    
    def get(self)->dict:
        return {
            'side': self.side,
            'price': self.price,
            'volume': self.volume,
            'timestamp': self.timestamp,
            'id': self.id,
        }


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
    
    def push(self, order: Order)->None:
        idx = bisect.bisect_right([o.price for o in self._orders], order.price)
        self._orders.insert(idx, order)
    

# from highest to lowest
class BidOrders(OrdersStack):
    def __init__(self):
        super().__init__()
    
    def push(self, order: Order)->None:
        idx = bisect.bisect_right([-o.price for o in self._orders], -order.price)
        self._orders.insert(idx, order)

        
        
#class OrderBook:
#    def __init__(self):
#        self.asks = AskOrders()
#        self.bids = BidOrders()
#    
#    def add(self, order:Order)->None:
#        if order['side']=='ask':
#            self.asks.push(order)
#        else:
#            self.bids.push(order)
#    
#    def get_best_ask(self)->float:
#        return self.asks.peek()
#    
#    def get_best_bid(self)->float:
#        return self.bids.peek()
    
    
if __name__ == "__main__":
#    ob = OrdersStack()
#    order = Order('ask', 100, 23)
#    print(order.get())
    orders = [
        Order('ask', 100, 23),
        Order('ask', 120, 23),
        Order('ask', 115, 23),
        Order('ask', 100, 23),
        Order('ask', 117, 23),
    ]
    ask = AskOrders()
    for order in orders:
        ask.push(order)
    print(ask.show())
    
    
    orders = [
        Order('bid', 100, 23),
        Order('bid', 120, 23),
        Order('bid', 115, 23),
        Order('bid', 100, 23),
        Order('bid', 117, 23),
    ]
    bid = BidOrders()
    for order in orders:
        bid.push(order)
    print(bid.show())
    
    
    