from decimal import Decimal
from enum import Enum

from typing import Literal, List, Optional, Union, Dict

from datetime import datetime
import uuid


class OrderStatus(Enum):
    NEW = 'new'
    PARTIALLY_FILLED = 'partially_filled' 
    FILLED = 'filled'
    CANCELLED = 'cancelled'


class OrderType(Enum):
    LIMIT = 'limit'
    MARKET = 'market'
    STOP = 'stop'
    

class OrderSide(Enum):
    BID = 'bid'
    ASK = 'ask'


class OrderTIF(Enum): # Time Force
    GTC = 'GTC' # Good Till Cancelled
    IOC = 'IOC' # Immediate Or Cancel
    FOK = 'FOK' # Fill Or Kill
    

class Order:
    __slots__ = (
        'id',
        'side',
        'price',
        'stop_price',
        'volume',
        'order_type',
        'time_in_force',
        'timestamp',
        'executed_volume',
        'last_execution_price',
        'status'
    )
    
    def __init__(self,
                 side: OrderSide,
                 volume: Union[int, Decimal],
                 price: Optional[Decimal]=None,
                 order_type: OrderType=OrderType.LIMIT,
                 stop_price: Optional[Decimal]=None,
                 time_in_force: OrderTIF=OrderTIF.GTC,
                ):
        
        self.side = side
        self.volume = volume
        self.order_type = order_type
        self.time_in_force = time_in_force
        
        if order_type==OrderType.MARKET:
            self.price = None
        elif order_type in [OrderType.LIMIT, OrderType.STOP] and price is None:
            raise ValueError(f'Price required for {order_type} order')
        else:
            self.price = price
        
        self.stop_price = stop_price
        if order_type==OrderType.STOP and stop_price is None:
            raise ValueError('Stop price required for stop order')
        
        if self.volume <=0:
            raise ValueError(f'Volume must be positive, got {volume}')
    
        self.timestamp = datetime.now()
        self.id = str(uuid.uuid4())
        
        self.executed_volume = 0
        self.status: OrderStatus = OrderStatus.NEW
        self.last_execution_price: Optional[Decimal] = None
    
    @property
    def remaining_volume(self) -> Union[int, Decimal]:
        return self.volume - self.executed_volume
    
    def execute(self, volume: Union[int, Decimal], price: Union[int, Decimal]) -> None:
        if volume > self.remaining_volume:
            raise ValueError(f'Cannot execute {volume}, remaining: {self.remaining_volume}')
        
        self.executed_volume += volume
        
        if self.executed_volume == self.volume:
            self.status = OrderStatus.FILLED
        elif self.executed_volume > 0:
            self.status = OrderStatus.PARTIALLY_FILLED
        
        self.last_execution_price = price
    
    def cancel(self) -> None:
        if self.status not in [OrderStatus.FILLED, OrderStatus.CANCELLED]:
            self.status = OrderStatus.CANCELLED
    
    def get(self)->dict:
        return {
            'id': self.id,
            'side': self.side.value,
            'price': self.price,
            'stop_price': self.stop_price,
            'volume': self.volume,
            'order_type': self.order_type.value,
            'time_in_force': self.time_in_force.value,
            'timestamp': self.timestamp.isoformat(),
            'executed_volume': self.executed_volume,
            'remaining_volume': self.remaining_volume,
            'status': self.status.value
        }
    
    def __repr__(self) -> str:
        price_str = f'@${self.price}' if self.price else '[MARKET]'
        return f'Order #{self.id[:8]} | {self.side.value} | {self.volume} | {price_str} | {self.status.value}'
    