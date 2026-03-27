from typing import List, Tuple, Optional, TYPE_CHECKING
from decimal import Decimal
import bisect
from collections import defaultdict

if TYPE_CHECKING:
    from .order import Order

from src.orderbook.stack import Stack


class StopOrdersStack(Stack):
    '''Base class for stop orders.'''
    
    def __init__(self):
        super().__init__()
        

class AskStopOrders(StopOrdersStack):
    '''Ask stop orders (sorted?) from lowest to highest price.'''
    
    def __init__(self):
        super().__init__()


class BidStopOrders(StopOrdersStack):
    '''Bid stop orders (sorted?) from highest to lowest price.'''
    
    def __init__(self):
        super().__init__()