import time
from typing import Literal
from datetime import datetime
import numpy as np

import pickle as pk


class Order:
    def __init__(self, side:Literal['bid', 'ask'], price:float, volume:int):
        self.side = side
        self.volume = volume
        self.timestamp = datetime.now()
    
    def get_data(self)->dict:
        return {
            'side': self.side,
            'volume': self.volume,
            'timestamp': self.timestamp
        }
    

class OrderBook:
    def __init__(self):
        self.storage = []
    
    def add(self, order:Order)->None:
        self.storage.append(order)
    
    def get_all(self)->list:
        return [obj.get_data() for obj in self.storage]


with open('orders', 'rb') as f:
    orders = pk.load(f)
    
print(len(orders))


# Generate Orders
#n=1_000
#dtype = [('type', 'U3'), ('price', 'f4'), ('quantity', 'i4')]
#
#types = np.random.choice(['bid', 'ask'], n)
#prices = np.round(np.random.uniform(1, 200, n), 2).astype('f4')
#quantities = np.random.randint(1, 100, n).astype('i4')
#
#orders = np.empty(n, dtype=dtype)
#orders['type'] = types
#orders['price'] = prices
#orders['quantity'] = quantities
#
#order_book = OrderBook()
#for order in orders:
#    order_book.add(Order(*order))
#    time.sleep(np.round(np.random.uniform(.1, 2.), 2))
#
#
#orders_list = order_book.get_all()
#
#with open('orders', 'wb') as f:
#    pk.dump(orders_list, f)
    
