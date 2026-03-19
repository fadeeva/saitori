import pytest

from decimal import Decimal
from datetime import datetime
import uuid

from src.order import *
from src.tradesbook import *
from src.orderlogger import *


logger = OrderLogger()

order_bid = Order(
    side=OrderSide.BID,
    price=10.54,
    volume=100,
    order_type=OrderType.LIMIT,
    logger=logger
)

order_ask = Order(
    side=OrderSide.ASK,
    price=10.54,
    volume=200,
    order_type=OrderType.LIMIT,
    logger=logger
)

def test_trade_creation():
    trade = Trade(
        order_ask, order_bid,
        OrderSide.BID,
        Decimal('10.54'), Decimal('100')
    )
    
    assert isinstance(trade.timestamp, datetime)
    assert trade.price == Decimal('10.54')
    assert trade.side is not OrderSide.ASK
    assert trade.volume == Decimal('100')
    

def test_tradebook_creation():
    tb = TradesBook()
    
    for side in [OrderSide.BID, OrderSide.ASK, OrderSide.BID]:
        tb.add(
            Trade(
                order_ask, order_bid,
                side,
                Decimal('10.54'), Decimal('100'))
        )
        
    assert tb is not None
    assert len(tb) == 3
        
    