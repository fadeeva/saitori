from decimal import Decimal
from datetime import datetime
import uuid

from src.order import Order, OrderSide


class Trade:
    def __init__(self,
                 order_a: Order, order_b: Order,
                 aggressor_side: OrderSide,
                 price: Decimal, volume: Decimal):
        
        self.bid_order_id = order_a.id if order_a.side == OrderSide.BID else order_b.id
        self.ask_order_id = order_a.id if order_a.side == OrderSide.ASK else order_b.id
        self.side = aggressor_side
        self.price = price
        self.volume = volume
        
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.now()
    
    def __str__(self):
        return f'#{self.id[:8]} | {datetime.fromtimestamp(timestamp)} \
                 | {self.bid_order_id[:8]} | {self.ask_order_id[:8]} \
                 | {self.aggressor_side} | {self.price} | {self.volume}'
    

class TradesBook:
    def __init__(self):
        self._trades = []
    
    def add(self, trade: Trade) -> None:
        self._trades.append(trade)
    
    def __len__(self):
        return len(self._trades)
    


