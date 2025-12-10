from typing import Literal
from datetime import datetime
import numpy as np


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


order = Order('ask', 123.43, 10)
order_book = OrderBook()
order_book.add(order)

print(order_book.get_all())

