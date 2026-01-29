import pytest
from datetime import datetime
from src.order import Order, OrderStatus, OrderType, OrderSide, OrderTimeForce


def test_order_creation_limit():
    ''' Test for limit order '''
    order = Order(
        side=OrderSide.BID,
        price=10.54,
        volume=100,
        order_type=OrderType.LIMIT
    )
    
    assert order.side == OrderSide.BID
    assert order.price == 10.54
    assert order.volume == 100
    assert order.order_type == OrderType.LIMIT
    assert order.time_in_force == OrderTimeForce.GTC
    assert order.remaining_volume == 100
    assert order.id is not None
    assert isinstance(order.timestamp, datetime)


def test_order_creation_market():
    ''' Test for market order '''
    order = Order(
        side=OrderSide.ASK,
        volume=55,
        order_type=OrderType.MARKET
    )
    
    assert order.side == OrderSide.ASK
    assert order.price is None # market order has no price
    assert order.volume == 55
    assert order.order_type == OrderType.MARKET
    

def test_order_creation_stop():
    ''' Test for stop-order '''
    order = Order(
        side=OrderSide.BID,
        price=105,
        stop_price=106.55,
        volume=150,
        order_type=OrderType.STOP
    )

    assert order.side == OrderSide.BID
    assert order.price == 105
    assert order.stop_price == 106.55
    assert order.volume == 150
    assert order.order_type == OrderType.STOP

    
def test_order_creation_validation():
    ''' Test of validation '''
    
    # Limit order without price - ERROR
    with pytest.raises(ValueError, match='Price required for OrderType.LIMIT'):
        Order(side=OrderSide.BID, volume=100, order_type=OrderType.LIMIT, price=None)
    
    # Stop order without stop_price - ERROR
    with pytest.raises(ValueError, match='Stop price required for stop order'):
        Order(side=OrderSide.BID, price=100, volume=100, order_type=OrderType.STOP, stop_price=None)
    
    # Stop order without price - ERROR (even if there is stop_price)
    with pytest.raises(ValueError, match='Price required for OrderType.STOP'):
        Order(side=OrderSide.BID, price=None, stop_price=100, volume=100, order_type=OrderType.STOP)
        
    # Negative volume - ERROR
    with pytest.raises(ValueError, match='Volume must be positive, got -100'):
        Order(side=OrderSide.BID, price=100, volume=-100, order_type=OrderType.LIMIT)
    

def test_order_execution():
    ''' Test for partial execution '''
    order = Order(side=OrderSide.BID, price=100, volume=100)
    
    order.execute(volume=30, price=99.95)
    
    assert order.executed_volume == 30
    assert order.remaining_volume == 70
    assert order.status == OrderStatus.PARTIALLY_FILLED
    assert hasattr(order, 'last_execution_price')
    assert order.last_execution_price == 99.95
    
    order.execute(volume=70, price=100.10)
    
    assert order.executed_volume == 100
    assert order.remaining_volume == 0
    assert order.status == OrderStatus.FILLED


def test_order_execution_validation():
    ''' Test of execution validation '''
    order = Order(side=OrderSide.BID, price=100, volume=100)
    
    # Try to execute more that it has
    with pytest.raises(ValueError, match='Cannot execute 150, remaining: 100'):
        order.execute(volume=150, price=100)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    