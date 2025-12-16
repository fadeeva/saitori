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
    
    def get_data(self)->dict:
        return {
            'side': self.side,
            'price': self.price,
            'volume': self.volume,
            'timestamp': self.timestamp
        }

    
class OrdersStack:
    def __init__(self, side:Literal['bid', 'ask']):
        self.side = side
        self.top = None
        self.stack = np.array([])
    
    def peek(self):
        return self.top
    
    def push(self, order:Order):
        if order.get_data()['side'] != self.side: return
        
        data = order.get_data()
        if self.top:
            if self.side=='ask' and self.top['price'] > data['price']:
                for o in self.stack:
                    if o.get_data()['price'] < data['price']:
                        idx = np.searchsorted(self.stack, o)
                        np.insert(self.stack, idx, order)
            else:
                self.stack = np.append(self.stack, [order])
                self.top = order.get_data()
        else:
            self.stack = np.append(self.stack, [order])
            self.top = order.get_data()
    
    def show_all(self):
        return [o.get_data() for o in self.stack]
            
        
        
class OrderBook:
    def __init__(self):
        self.asks = OrdersStack('ask')
        self.bids = OrdersStack('bid')
    
    def add(self, order:Order)->None:
        if order['side']=='ask':
            self.asks.push(order)
        else:
            self.bids.push(order)
    
    def get_asks(self)->list:
        sorted_asks = sorted(self.asks, key=lambda order: (order['price'], order['timestamp']))
        return sorted_asks
    
    def get_bids(self)->list:
        sorted_bids = sorted(self.bids, key=lambda order: (order['price'], order['timestamp']), reverse=True)
        return sorted_bids
    
    def get_best_ask(self)->float:
        return self.asks.peek()
    
    def get_best_bid(self)->float:
        return self.bids.peek()
    
    
order_stack = OrdersStack('ask')

order = Order('ask', 123.32, 23)
order_stack.push(order)
time.sleep(1)
order = Order('ask', 225.90, 23)
order_stack.push(order)

print(order_stack.show_all())    
    

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
    
