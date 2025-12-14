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
    

class OrderBook:
    def __init__(self):
        self.asks = []
        self.bids = []
    
    def add(self, order:tuple)->None:
        if order['side']=='ask':
            self.asks.append(order)
        else:
            self.bids.append(order)
    
    def get_asks(self)->list:
        return self.asks
    
    def get_bids(self)->list:
        return self.bids


with open('orders', 'rb') as f:
    orders = pk.load(f)

keys = ['side', 'price', 'volume', 'timestamp']
order_book = OrderBook()
for order in orders:
    order_book.add(dict(zip(keys, order)))

#print(order_book.get_asks())


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
    
