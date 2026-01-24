import pytest
from datetime import datetime
from src.order import Order


def test_order_creation_limit():
    ''' Test for limit order '''
    order = Order(
        side='bid',
        price=10.54,
        volume=100,
        order_type='limit'
    )
    
    assert order.side == 'bid'
    assert order.price == 10.54
    assert order.volume == 100
    assert order.order_type == 'limit'
    assert order.time_in_force == 'GTC'
    assert order.remaining_volume == 100
    assert order.id is not None
    assert isinstance(order.timestamp, datetime)


def test_order_creation_market():
    ''' Test for market order '''
    order = Order(
        side='ask',
        volume=55,
        order_type='market'
    )
    
    assert order.side == 'ask'
    assert order.price is None # market order has no price
    assert order.volume == 55
    assert order.order_type == 'market'
    
    