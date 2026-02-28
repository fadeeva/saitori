from decimal import Decimal
from datetime import datetime
import uuid

from src.order import Order, OrderSide


class Trade:
    def __init__(self,
                 bid_order_id: str, ask_order_id: str,
                 aggressor_side: OrderSide,
                 price: Decimal, volume: Decimal):
        self.bid_order_id = bid_order_id
        self.ask_order_id = ask_order_id
        self.side = aggressor_side
        self.price = price
        self.volume = volume
        
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.now()
    

class TradesBook:
    def __init__(self):
        self._trades = []
    
    def add(self, trade: Trade) -> None:
        self._trades.append(trade)
    
    def __len__(self):
        return len(self._trades)


