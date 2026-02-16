import pytest
from datetime import datetime
from src.order import *
from src.orderbook import *


def test_orderbook_creation():
    limit_buy = Order(
        side=OrderSide.BID,
        price=Decimal('100.50'),
        volume=Decimal('100'),
        order_type=OrderType.LIMIT,
        time_in_force=OrderTIF.GTC
    )

    limit_sell = Order(
        side=OrderSide.ASK,
        price=Decimal('110.00'),
        volume=Decimal('100'),
        order_type=OrderType.LIMIT,
        time_in_force=OrderTIF.IOC
    )

    ob = OrderBook()
    ob.add(limit_buy)
    ob.add(limit_sell)

    assert isinstance(ob.best_bid, Order)
    assert isinstance(ob.best_ask, Order)
    assert ob.best_bid is limit_buy
    assert ob.best_ask is not limit_buy
    assert len(ob) == 2
    
    
def test_orderbook_execution():
    ob = OrderBook()
    
    orders = [
        (Decimal('120.00'), Decimal(50)),
        (Decimal('115.00'), Decimal(30)),
        (Decimal('110.00'), Decimal(20)),
        (Decimal('105.00'), Decimal(10)),
        (Decimal('100.00'), Decimal(5)),
    ]
    
    for price, volume in orders:
        ob.add(
            Order(
                side=OrderSide.BID,
                price=price,
                volume=volume,
                order_type=OrderType.LIMIT,
                time_in_force=OrderTIF.GTC
            )
        )
    
    limit_sell = Order(
        side=OrderSide.ASK,
        price=Decimal('110.00'),
        volume=Decimal('120'),
        order_type=OrderType.LIMIT,
        time_in_force=OrderTIF.IOC
    )
    
    ob.add(limit_sell)
    
    assert len(ob) == 3
    
    