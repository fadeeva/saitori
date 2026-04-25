import pytest
from datetime import datetime

from src.order import *
from src.orderbook.stop_orderbook import *
from src.orderlogger import *


logger = OrderLogger()

def test_orderbook_creation():
    stop_buy = Order( # LIMIT
        side=OrderSide.BID,
        stop_price=Decimal('100.50'),
        price=Decimal('105.50'),
        volume=Decimal('100'),
        order_type=OrderType.STOP,
        time_in_force=OrderTIF.GTC,
        logger=logger
    )

    stop_sell = Order( # MARKET
        side=OrderSide.ASK,
        stop_price=Decimal('110.00'),
        volume=Decimal('100'),
        order_type=OrderType.STOP,
        time_in_force=OrderTIF.GTC,
        logger=logger
    )

    ob = StopOrderBook()
    ob.add_to_storage(stop_buy)
    ob.add_to_storage(stop_sell)

    assert ob.storage_len == 2

def test_orders_activation():
    ob = StopOrderBook()
    
    for i in range(10):
        ob.add_to_storage(
            Order(
                side=OrderSide.ASK if i%2 else OrderSide.BID,
                stop_price=Decimal('100.00') if i%2 else Decimal('120.00'),
                volume=Decimal('20'),
                order_type=OrderType.STOP,
                time_in_force=OrderTIF.GTC,
                logger=logger
            )
        )

    assert ob.storage_len == 10
    assert len(ob.get_activated(Decimal('100.00'))) == 5
    assert ob.storage_len == 5
    
    

    