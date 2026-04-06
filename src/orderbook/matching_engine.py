from decimal import Decimal
from typing import Literal, List, Optional, Union, Dict, Tuple, Iterator, TYPE_CHECKING
import bisect
from collections import defaultdict

if TYPE_CHECKING:
    from .order import Order
    from src.orderbook.ordersstack import OrdersStack
    from src.orderbook.ordersstack import StopOrdersStack
    from src.orderbook.stopordersstack import AskStopOrders, BidStopOrders
    from src.orderbook.ordersstack import AskOrders, BidOrders

from src.order import OrderSide, OrderTIF


class MatchingEngine:
    def add(self, order: 'Order',
            asks: Optional['AskOrders', 'AskStopOrders'],
            bids: Optional['BidOrders', 'BidStopOrders']) -> None:
        pass