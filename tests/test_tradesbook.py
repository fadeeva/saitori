import pytest

from decimal import Decimal
from datetime import datetime

from src.order import *
from src.tradesbook import *


def test_trade_creation():
    bid = Order(
        side=OrderSide.BID,
        price=Decimal('10.54'),
        volume=Decimal('100'),
        order_type=OrderType.LIMIT
    )
    
    ask = Order(
        side=OrderSide.ASK,
        price=Decimal('10.54'),
        volume=Decimal('100'),
        order_type=OrderType.LIMIT
    )
    
    trade = Trade(
        bid.id, ask.id,
        OrderSide.ASK,
        Decimal('10.54'), Decimal('100')
    )
    
    assert isinstance(trade.timestamp, datetime)
    assert trade.price == Decimal('10.54')
    assert trade.side == OrderSide.ASK
    assert trade.volume == Decimal('100')