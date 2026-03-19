from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Literal, List, Optional, Union, Dict, Tuple, Iterator
from collections import defaultdict

from src.order import Order, OrderStatus, OrderType, OrderSide, OrderTIF, OrderErrorMessages


@dataclass(frozen=True)
class OrderSnapshot:
    '''Single snapshot from order'''
    
    status: str
    side: str
    type: str
    tif: str
    volume: Decimal
    price: Decimal
    stop_price: Decimal
    executed_volume: Decimal
    remaining_volume: Decimal
    timestamp: datetime

    @classmethod
    def from_order(cls, order: Order):
        return cls(
            status=order.status.value,
            side=order.side.value,
            type=order.order_type.value,
            tif=order.time_in_force.value,
            volume=order.volume,
            price=order.price,
            stop_price=order.stop_price,
            executed_volume=order.executed_volume,
            remaining_volume=order.remaining_volume,
            timestamp=datetime.now()
        )


class OrderLogger:
    '''Records all order snapshots for audit and analysis.'''
    
    def __init__(self):
        self._logs: defaultdict[str, List[Order]] = defaultdict(list)
    
    def add(self, order: Order):
        self._logs[order.id].append(OrderSnapshot.from_order(order))
    
    def show_by_id(self, id:str) -> List[Order]:
        return self._logs[id]
    
    def show(self) -> Dict[str, List[Order]]:
        return dict(self._logs)
    
#    def __str__(self):
#        out = 'LOGGER:\n'
#        for key, values in self._logs.items():
#            out += f'ID: {key}\n'
#            for o in values:
#                out += f'\t{o}\n'
#        
#        return out
    
        