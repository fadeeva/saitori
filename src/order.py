from typing import Literal, List, Optional, Union, Dict
from datetime import datetime

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
        
        if self.volume <=0:
            raise ValueError(f'Volume must be positive, got {volume}')
        
                             
        self.timestamp = datetime.now()
        self.id = str(uuid.uuid4())
        
        self.executed_volume = 0
        self.status: Literal['new', 'partially_filled', 'filled', 'cancelled'] = 'new'
    
    @property
    def remaining_volume(self) -> Union[int, float]:
        return self.volume - self.executed_volume
    
    def execute(self, volume: Union[int, float], price: float) -> None:
        if volume > self.remaining_volume:
            raise ValueError(f'Cannot execute {volume}, remaining: {self.remaining_volume}')
        
        self.executed_volume += volume
        
        if self.executed_volume == self.volume:
            self.status = 'filled'
        elif self.executed_volume > 0:
            self.status = 'partially_filled'
        
        self.last_execution_price = price
    
    def cancel(self) -> None:
        if self.status not in ['filled', 'cancelled']:
            self.status = 'cancelled'
    
    def get(self)->dict:
        return {
            'id': self.id,
            'side': self.side,
            'price': self.price,
            'stop_price': self.stop_price,
            'volume': self.volume,
            'order_type': self.order_type,
            'time_in_force': self.time_in_force,
            'timestamp': self.timestamp.isoformat(),
            'executed_volume': self.executed_volume,
            'remaining_volume': self.remaining_volume,
            'status': self.status
        }
    
    def __repr__(self) -> str:
        price_str = f'@${self.price}' if self.price else '[MARKET]'
        return f'Order #{self.id[:8]} | {self.side} | {self.volume} | {price_str} | {self.status}'
    