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
    

def test_order_creation_stop():
    ''' Test for stop-order '''
    order = Order(
        side='bid',
        price=105,
        stop_price=106.55,
        volume=150,
        order_type='stop'
    )

    assert order.side == 'bid'
    assert order.price == 105
    assert order.stop_price == 106.55
    assert order.volume == 150
    assert order.order_type == 'stop'

    
def test_order_creation_validation():
    ''' Test of validation '''
    
    # Limit order without price - ERROR
    with pytest.raises(ValueError, match='Price required for limit order'):
        Order(side='bid', volume=100, order_type='limit', price=None)
    
    # Stop order without stop_price - ERROR
    with pytest.raises(ValueError, match='Stop price required for stop order'):
        Order(side='bid', price=100, volume=100, order_type='stop', stop_price=None)
    
    # Stop order without цены - ERROR (even if there is stop_price)
    with pytest.raises(ValueError, match='Price required for stop order'):
        Order(side='bid', price=None, stop_price=100, volume=100, order_type='stop')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    