from decimal import Decimal
from datetime import datetime

from order import Order, OrderSide


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
        self.timestamp = datetime.now()
    

class TradesBook:
    def __init__(self):
        self._trades = []
    
    def add(self, trade: Trade) -> None:
        self._trades.append(trade)


