from decimal import Decimal
from typing import Literal, List, Optional, Union, Dict, Tuple, Iterator
from collections import defaultdict
import copy

from order import Order, OrderStatus, OrderType, OrderSide, OrderTIF, OrderErrorMessages # добавить src. позже в начало, а то нихуя работать не будет


class OrderLogger:
    def __init__(self):
        self._logs: defaultdict[str, List[Order]] = defaultdict(list)
    
    def add(self, order: Order):
        self._logs[order.id].append(copy.deepcopy(order)) # нужно будет доавить dataclass для snapshots? нужно думать
    
    def __str__(self):
        out = 'LOGGER:\n'
        for key, values in self._logs.items():
            out += f'{key}\n'
            for o in values:
                out += f'{o.get()}\n'
        
        return out
    
    

ol = OrderLogger()
o = Order(side=OrderSide.BID, price=100, volume=100)
ol.add(o)
o.status = OrderStatus.FILLED
ol.add(o)

print(ol)
        