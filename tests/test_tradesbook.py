import pytest

from decimal import Decimal
from datetime import datetime
import uuid

from src.order import *
from src.tradesbook import *


def test_trade_creation():
    order_a = Order(
        side=OrderSide.BID,
        price=10.54,
        volume=100,
        order_type=OrderType.LIMIT
    )
    
    order_b = Order(
        side=OrderSide.ASK,
        price=10.54,
        volume=200,
        order_type=OrderType.LIMIT
    )
    
    trade = Trade(
        order_a, order_b,
        OrderSide.BID,
        Decimal('10.54'), Decimal('100')
    )
    
    assert isinstance(trade.timestamp, datetime)
    assert trade.price == Decimal('10.54')
    assert trade.side is not OrderSide.ASK
    assert trade.volume == Decimal('100')
    

def test_tradebook_creation():
    pass
    