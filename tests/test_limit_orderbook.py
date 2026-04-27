import pytest
from datetime import datetime

from src.order import *
from src.orderbook.limit_orderbook import *
from src.orderlogger import *


logger = OrderLogger()

def test_orderbook_creation():
    limit_buy = Order(
        side=OrderSide.BID,
        price=Decimal('100.50'),
        volume=Decimal('100'),
        order_type=OrderType.LIMIT,
        time_in_force=OrderTIF.GTC,
        logger=logger
    )

    limit_sell = Order(
        side=OrderSide.ASK,
        price=Decimal('110.00'),
        volume=Decimal('100'),
        order_type=OrderType.LIMIT,
        time_in_force=OrderTIF.GTC,
        logger=logger
    )

    ob = LimitOrderBook()
    ob.add(limit_buy)
    ob.add(limit_sell)

    assert isinstance(ob.best_bid, Order)
    assert isinstance(ob.best_ask, Order)
    assert ob.best_bid is limit_buy
    assert ob.best_ask is not limit_buy
    assert len(ob) == 2
    
    
def test_orderbook_execution():
    ob = LimitOrderBook()
    
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
                time_in_force=OrderTIF.GTC,
                logger=logger
            )
        )
    
    limit_sell = Order(
        side=OrderSide.ASK,
        price=Decimal('110.00'),
        volume=Decimal('120'),
        order_type=OrderType.LIMIT,
        time_in_force=OrderTIF.GTC,
        logger=logger
    )
    
    ob.add(limit_sell)
    
    assert len(ob) == 3
    assert ob.best_ask.remaining_volume == Decimal('20')
    assert ob.best_bid.price == Decimal('105.00')
    
    # ==================================================
    
    ob = LimitOrderBook()
    
    orders = [
        (Decimal('100.00'), Decimal(5)),
        (Decimal('105.00'), Decimal(10)),
        (Decimal('110.00'), Decimal(20)),
        (Decimal('115.00'), Decimal(30)),
        (Decimal('120.00'), Decimal(50)),
    ]
    
    for price, volume in orders:
        ob.add(
            Order(
                side=OrderSide.ASK,
                price=price,
                volume=volume,
                order_type=OrderType.LIMIT,
                time_in_force=OrderTIF.GTC,
                logger=logger
            )
        )
    
    limit_sell = Order(
        side=OrderSide.BID,
        price=Decimal('110.00'),
        volume=Decimal('120'),
        order_type=OrderType.LIMIT,
        time_in_force=OrderTIF.GTC,
        logger=logger
    )
    
    ob.add(limit_sell)
    
    assert len(ob) == 3
    assert ob.best_bid.remaining_volume == Decimal('85')
    assert ob.best_ask.price == Decimal('115.00')
    
    # ==================================================
    
    ob = LimitOrderBook()
    
    orders = [
        (Decimal('100.00'), Decimal(5), OrderSide.ASK),
        (Decimal('105.00'), Decimal(10), OrderSide.ASK),
        (Decimal('110.00'), Decimal(20), OrderSide.BID),
        (Decimal('115.00'), Decimal(30), OrderSide.ASK),
        (Decimal('120.00'), Decimal(50), OrderSide.BID),
        (Decimal('100.00'), Decimal(5), OrderSide.BID),
        (Decimal('105.00'), Decimal(10), OrderSide.ASK),
        (Decimal('110.00'), Decimal(20), OrderSide.ASK),
        (Decimal('115.00'), Decimal(30), OrderSide.BID),
        (Decimal('120.00'), Decimal(50), OrderSide.ASK),
    ]
    
    
    for price, volume, side in orders:
        ob.add(
            Order(
                side=side,
                price=price,
                volume=volume,
                order_type=OrderType.LIMIT,
                time_in_force=OrderTIF.GTC,
                logger=logger
            )
        )
    
    assert len(ob) == 3
    assert ob.best_ask.price == Decimal('120.00')
    assert ob.best_ask.volume == Decimal('50')
    assert ob.best_bid.price == Decimal('115.00')
    assert ob.best_bid.remaining_volume == Decimal('25')


def test_FOK_execution():
    ob = LimitOrderBook()
    
    limit_buy = Order(
        side=OrderSide.BID,
        price=Decimal('110.00'),
        volume=Decimal('100'),
        order_type=OrderType.LIMIT,
        time_in_force=OrderTIF.GTC,
        logger=logger
    )

    limit_sell = Order(
        side=OrderSide.ASK,
        price=Decimal('110.00'),
        volume=Decimal('120'),
        order_type=OrderType.LIMIT,
        time_in_force=OrderTIF.FOK,
        logger=logger
    )

    ob.add(limit_buy)
    ob.add(limit_sell)
    
    assert len(ob) == 1
    assert ob.best_bid.volume == 100
    assert ob.best_ask is None
    
    # ==================================================
    
    ob = LimitOrderBook()
    orders = [
        (Decimal('100.00'), Decimal(5)),
        (Decimal('105.00'), Decimal(10)),
        (Decimal('110.00'), Decimal(20)),
        (Decimal('115.00'), Decimal(30)),
        (Decimal('120.00'), Decimal(50)),
    ]
    
    for price, volume in orders:
        ob.add(
            Order(
                side=OrderSide.ASK,
                price=price,
                volume=volume,
                order_type=OrderType.LIMIT,
                time_in_force=OrderTIF.GTC,
                logger=logger
            )
        )
    
    limit_buy = Order(
        side=OrderSide.BID,
        price=Decimal('110.00'),
        volume=Decimal('120'),
        order_type=OrderType.LIMIT,
        time_in_force=OrderTIF.FOK,
        logger=logger
    )
    
    ob.add(limit_buy)
    
    assert len(ob) == 5
    assert ob.best_bid is None
    
    # ==================================================
    
    ob = LimitOrderBook()
    orders = [
        (Decimal('100.00'), Decimal(5)),
        (Decimal('105.00'), Decimal(10)),
        (Decimal('110.00'), Decimal(20)),
        (Decimal('115.00'), Decimal(30)),
        (Decimal('120.00'), Decimal(90)),
    ]
    
    for price, volume in orders:
        ob.add(
            Order(
                side=OrderSide.BID,
                price=price,
                volume=volume,
                order_type=OrderType.LIMIT,
                time_in_force=OrderTIF.GTC,
                logger=logger
            )
        )
    
    limit_sell = Order(
        side=OrderSide.ASK,
        price=Decimal('110.00'),
        volume=Decimal('140'),
        order_type=OrderType.LIMIT,
        time_in_force=OrderTIF.FOK,
        logger=logger
    )
    
    ob.add(limit_sell)
    
    assert len(ob) == 2
    assert ob.best_ask is None

    
def test_IOC_execution():
    ob = LimitOrderBook()
    
    limit_sell = Order(
        side=OrderSide.ASK,
        price=Decimal('100.00'),
        volume=Decimal('80'),
        order_type=OrderType.LIMIT,
        time_in_force=OrderTIF.GTC,
        logger=logger
    )
    
    ob.add(limit_sell)
    
    limit_buy = Order(
        side=OrderSide.BID,
        price=Decimal('100.00'),
        volume=Decimal('100'),
        order_type=OrderType.LIMIT,
        time_in_force=OrderTIF.IOC,
        logger=logger
    )
    
    ob.add(limit_buy)
    
    assert len(ob) == 0
    assert ob.best_bid is None
    assert ob.best_ask is None

    
def test_mixed_orders_execution():
    ob = LimitOrderBook()
    
    orders = [
        (OrderSide.ASK, Decimal('110.00'), Decimal(150), OrderTIF.GTC),
        (OrderSide.BID, Decimal('105.00'), Decimal(10), OrderTIF.FOK),
        (OrderSide.ASK, Decimal('110.00'), Decimal(20), OrderTIF.IOC),
        (OrderSide.ASK, Decimal('115.00'), Decimal(30), OrderTIF.FOK),
        (OrderSide.BID, Decimal('120.00'), Decimal(90), OrderTIF.IOC),
    ]
    
    for side, price, volume, tif in orders:
        ob.add(
            Order(
                side=side,
                price=price,
                volume=volume,
                order_type=OrderType.LIMIT,
                time_in_force=tif,
                logger=logger
            )
        )
        
    assert len(ob) == 1
    assert ob.best_ask.remaining_volume == Decimal(60)


def test_market_order_execution():
    ob = LimitOrderBook()
    
    orders = [
        (Decimal('100.00'), Decimal(15)),
        (Decimal('105.00'), Decimal(20)),
        (Decimal('110.00'), Decimal(30)),
    ]
    
    for price, volume in orders:
        ob.add(
            Order(
                side=OrderSide.ASK,
                price=price,
                volume=volume,
                order_type=OrderType.LIMIT,
                time_in_force=OrderTIF.GTC,
                logger=logger
            )
        )
    
    # FOK-order
    market_order = Order(
        side=OrderSide.BID,
        volume=25,
        order_type=OrderType.MARKET,
        time_in_force=OrderTIF.FOK,
        logger=logger
    )
    
    ob.add(market_order)
    
    assert len(ob) == 2
    assert ob.best_bid is None
    assert ob.best_ask.remaining_volume == Decimal(10)
    
    ob.clear()
    for price, volume in orders:
        ob.add(
            Order(
                side=OrderSide.ASK,
                price=price,
                volume=volume,
                order_type=OrderType.LIMIT,
                time_in_force=OrderTIF.GTC,
                logger=logger
            )
        )
    
    # IOC-order
    market_order = Order(
        side=OrderSide.BID,
        volume=125,
        order_type=OrderType.MARKET,
        time_in_force=OrderTIF.IOC,
        logger=logger
    )
    
    ob.add(market_order)
    
    assert len(ob) == 0
    assert market_order.status == OrderStatus.PARTIALLY_FILLED
    

def test_clear_LimitOrderBook():
    ob = LimitOrderBook()
    
    orders = [
        (Decimal('100.00'), Decimal(5)),
        (Decimal('105.00'), Decimal(10)),
        (Decimal('110.00'), Decimal(20)),
        (Decimal('115.00'), Decimal(30)),
        (Decimal('120.00'), Decimal(50)),
    ]
    
    for price, volume in orders:
        ob.add(
            Order(
                side=OrderSide.ASK,
                price=price,
                volume=volume,
                order_type=OrderType.LIMIT,
                time_in_force=OrderTIF.GTC,
                logger=logger
            )
        )
    
    assert len(ob) == 5
    ob.clear()
    assert len(ob) == 0
    
    