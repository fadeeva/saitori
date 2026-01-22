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
        self.price = price
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
        
        self.timestamp = datetime.now()
        self.id = str(uuid.uuid4())
    
    def get(self)->dict:
        return {
            'id': self.id,
            'side': self.side,
            'price': self.price,
            'volume': self.volume,
            'timestamp': self.timestamp,
        }
