from decimal import Decimal
from typing import Literal, List, Optional, Union, Dict, Tuple, Iterator
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

from order import Order, OrderStatus, OrderType, OrderSide, OrderTIF, OrderErrorMessages # добавить src. позже в начало, а то нихуя работать не будет


@dataclass(frozen=True)
class OrderSnapshot:
    status: str
    side: str
    type: str
    tif: str
    volume: Decimal
    price: Decimal
    executed_volume: Decimal
    remaining_volume: Decimal
    timestamp: datetime

    @classmethod
    def from_order(cls, order: Order):
        # check price for stop order
        return cls(
            status=order.status.value,
            side=order.side.value,
            type=order.order_type.value,
            tif=order.time_in_force.value,
            volume=order.volume,
            price=order.price,
            executed_volume=order.executed_volume,
            remaining_volume=order.remaining_volume,
            timestamp=datetime.now()
        )


class OrderLogger:
    def __init__(self):
        self._logs: defaultdict[str, List[Order]] = defaultdict(list)
    
    def add(self, order: Order):
        self._logs[order.id].append(OrderSnapshot.from_order(order))
    
    def __str__(self):
        out = 'LOGGER:\n'
        for key, values in self._logs.items():
            out += f'ID: {key}\n'
            for o in values:
                out += f'\t{o}\n'
        
        return out
    
    

ol = OrderLogger()
o = Order(side=OrderSide.BID, price=100, volume=100)
ol.add(o)
o.status = OrderStatus.FILLED
ol.add(o)

print(ol)
        