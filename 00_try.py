from typing import Literal, List, Optional, Union, Dict
from datetime import datetime

import bisect
import uuid


class Order:
    def __init__(self,
                 side: Literal['bid', 'ask'],
                 volume: Union[int, float],
                 price: Optional[float]=None,
                 order_type: Literal['limit', 'market', 'stop']='limit',
                 stop_price: Optional[float]=None,
                 time_in_force: Literal['GTC', 'IOC', 'FOK']='GTC',
                 # GTC (Good Till Cancelled)
                 # IOC (Immediate Or Cancel)
                 # FOK (Fill Or Kill)
                ):
        
        self.side = side
        self.volume = volume
        self.price = price
        self.order_type = order_type
        self.time_in_force = time_in_force
        
        if order_type=='market':
            self.price = None
        elif order_type in ['limit', 'stop'] and price is None:
            raise ValueError(f'Price required for {order_type} order')
        else:
            self.price = price
        
        if order_type=='stop' and stop_price is None:
            raise ValueError('Stop price required for stop order')
        else:
            self.stop_price = stop_price
        
        self.timestamp = datetime.now()
        self.id = str(uuid.uuid4())
    
    def get(self)->dict:
        return {
            'id': self.id,
            'side': self.side,
            'price': self.price,
            'volume': self.volume,
            'timestamp': self.timestamp,
        }


class OrdersStack:
    def __init__(self):
        self._orders: List[Order] = []
    
    def peek(self)->Optional[Order]:
        return self._orders[-1].get() if self._orders else None
    
    def show(self)->List[dict]:
        return [o.get() for o in self._orders]
    
    def select(self, by:Literal['price', 'volume'], value:Union[int, float])->Optional[Order]:
        if self._orders:
            params = self.peek().keys()
            if by in params:
                return [o.get() for o in self._orders if o.get()[by]==value]
        
        return []


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
        if order.side=='ask':
            self.asks.push(order)
        else:
            self.bids.push(order)
    
    def get_best_ask(self)->Optional[Order]:
        return self.bids.peek()
    
    def get_best_bid(self)->Optional[Order]:
        return self.bids.peek()
    
    def get_price(self, price:float)->Optional[Order]:
        return [self.asks.select('price', price), self.bids.select('price', price)]
    
    
if __name__ == "__main__":
#    ob = OrdersStack()
    order = Order('ask', 100, 23)
    print(order.get())
#    orders = [
#        Order('bid', 117, 23),
#        Order('ask', 100, 49),
#        Order('ask', 120, 12),
#        Order('bid', 120, 8),
#        Order('ask', 115, 21),
#        Order('ask', 117, 19),
#        Order('bid', 100, 11),
#        Order('ask', 100, 5),
#        Order('bid', 115, 5),
#        Order('bid', 100, 10),
#        
#    ]
#    book = OrderBook()
#    for order in orders:
#        book.add(order)
#    print(book.get_best_ask())
#    print(book.get_best_bid())
    
#    print('=================')
#    print(book.get_price(100))
    
    
    