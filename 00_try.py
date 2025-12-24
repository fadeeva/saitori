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
        return self._orders[-1].get() if self._orders else None
    
    def show(self)->List[dict]:
        return [o.get() for o in self._orders]
    
    def select(self, price:float)->Optional[Order]:
        return [o.get() for o in self._orders if o.get()['price']==price]


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

        
class OrderBook:
    def __init__(self):
        self.asks = AskOrders()
        self.bids = BidOrders()
    
    def add(self, order:Order)->None:
        if order.side=='ask':
            self.asks.push(order)
        else:
            self.bids.push(order)
    
    def get_best_ask(self)->Optional[Order]:
        price = self.asks.peek()['price']
        return self.asks.select({'price': price})
    
    def get_best_bid(self)->Optional[Order]:
        return self.bids.peek()
    
    def get_price(self, price:float)->Optional[Order]:
        return [self.asks.select(price), self.bids.select(price)]
    
    
if __name__ == "__main__":
#    ob = OrdersStack()
#    order = Order('ask', 100, 23)
#    print(order.get())
    orders = [
        Order('bid', 117, 23),
        Order('ask', 100, 49),
        Order('ask', 120, 12),
        Order('bid', 120, 8),
        Order('ask', 115, 21),
        Order('ask', 117, 19),
        Order('bid', 100, 11),
        Order('ask', 100, 5),
        Order('bid', 115, 5),
        Order('bid', 100, 10),
        
    ]
    book = OrderBook()
    for order in orders:
        book.add(order)
    print(book.get_best_ask())
    print(book.get_best_bid())
    
    print('=================')
    print(book.get_price(100))
    
    
    