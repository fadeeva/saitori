import time
from typing import Literal
from datetime import datetime
import numpy as np

import pickle as pk


class Order:
    def __init__(self,
                 side:Literal['bid', 'ask'], price:float, volume:int):
        self.side = side
        self.volume = volume
        self.price = price
        self.timestamp = datetime.now()
    
    def get(self)->dict:
        return {
            'side': self.side,
            'price': self.price,
            'volume': self.volume,
            'timestamp': self.timestamp
        }


class OrdersStack:
    def __init__(self):
        self.top = None
        self.stack = np.array([])
    
    def peek(self):
        return self.top
    
    def show(self):
        return self.stack


# from lowest to highest 
class AskOrders(OrdersStack):
    def __init__(self):
        super().__init__()
    
    def push(self, order: Order)->None:
        if self.top:
            for o in self.stack:
                if o['price'] > order.get()['price']:
                    self.stack = np.insert(self.stack, np.where(self.stack==o)[0], order.get())
                    self.top = self.stack[-1]
                    return
                    
        self.stack = np.append(self.stack, [order.get()])
        self.top = self.stack[-1]
    

#ask = AskOrders()
#order = Order('ask', 100, 23)
#ask.push(order)
#order = Order('ask', 120, 23)
#ask.push(order)
#order = Order('ask', 115, 23)
#ask.push(order)
#order = Order('ask', 100, 23)
#ask.push(order)
#order = Order('ask', 117, 23)
#ask.push(order)
#print(ask.show())

# from highest to lowest
class BidOrders(OrdersStack):
    def __init__(self):
        super().__init__()
    
    def push(self, order: Order)->None:
        if self.top:
            for o in self.stack:
                if o['price'] < order.get()['price']:
                    self.stack = np.insert(self.stack, np.where(self.stack==o)[0], order.get())
                    self.top = self.stack[-1]
                    return
                    
        self.stack = np.append(self.stack, [order.get()])
        self.top = self.stack[-1]
        

bid = BidOrders()
order = Order('bid', 100, 23)
bid.push(order)
order = Order('bid', 120, 23)
bid.push(order)
order = Order('bid', 115, 23)
bid.push(order)
order = Order('bid', 100, 23)
bid.push(order)
order = Order('bid', 117, 23)
bid.push(order)
print(bid.show())
        
        
class OrderBook:
    def __init__(self):
        self.asks = AskOrders()
        self.bids = BidOrders()
    
    def add(self, order:Order)->None:
        if order['side']=='ask':
            self.asks.push(order)
        else:
            self.bids.push(order)
    
#    def get_asks(self)->list:
#        sorted_asks = sorted(self.asks, key=lambda order: (order['price'], order['timestamp']))
#        return sorted_asks
#    
#    def get_bids(self)->list:
#        sorted_bids = sorted(self.bids, key=lambda order: (order['price'], order['timestamp']), reverse=True)
#        return sorted_bids
    
    def get_best_ask(self)->float:
        return self.asks.peek()
    
    def get_best_bid(self)->float:
        return self.bids.peek()
    


#with open('orders', 'rb') as f:
#    orders = pk.load(f)
#
#keys = ['side', 'price', 'volume', 'timestamp']
#order_book = OrderBook()
#for order in orders:
#    order_book.add(dict(zip(keys, order)))
#
#print(order_book.get_best_ask())
#print(order_book.get_best_bid())


# Generate Orders
#n=1_000
#dtype = [
#    ('type', 'U3'),
#    ('price', 'f4'),
#    ('quantity', 'i4'),
#    ('timestamp', 'datetime64[ns]')
#]
#
#types = np.random.choice(['bid', 'ask'], n)
#prices = np.round(np.random.uniform(1, 200, n), 2).astype('f4')
#quantities = np.random.randint(1, 100, n).astype('i4')
#
#timestamps = []
#for i in range(n):
#    timestamps.append(datetime.now())
#    time.sleep(np.round(np.random.uniform(.1, 2.), 2))
#
#orders = np.empty(n, dtype=dtype)
#orders['type'] = types
#orders['price'] = prices
#orders['quantity'] = quantities
#orders['timestamp'] = np.array(timestamps)
#
#with open('orders', 'wb') as f:
#    pk.dump(orders, f)
    
