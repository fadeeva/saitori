import pytest

from decimal import Decimal
from datetime import datetime
import uuid

from src.order import *
from src.tradesbook import *


def test_trade_creation():
    trade = Trade(
        str(uuid.uuid4()), str(uuid.uuid4()),
        OrderSide.ASK,
        Decimal('10.54'), Decimal('100')
    )
    
    assert isinstance(trade.timestamp, datetime)
    assert trade.price == Decimal('10.54')
    assert trade.side == OrderSide.ASK
    assert trade.volume == Decimal('100')
    

def test_tradebook_creation():
    pass
    