from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order import Order

from src.orderbook.stop_orders_stack import AskStopOrders, BidStopOrders
from src.orderbook.orderbook import OrderBook


class StopOrderBook(OrderBook):
    '''Order book matching bids and asks with price-time priority for stop orders.'''
    
    def __init__(self):
        super().__init__(AskStopOrders(), BidStopOrders())
    
    
    
    
    
    
    
            
    

    
