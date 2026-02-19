from decimal import Decimal

try:
    from src.order import Order, OrderStatus, OrderType, OrderSide, OrderTIF, OrderErrorMessages
    from src.orderbook import OrderBook, BidOrders, AskOrders, OrdersStack
    
    IMPORT_SUCCESS = True
except ImportError as e:
    print(f'Import Error: {e}.')
    IMPORT_SUCCESS = False
    
    
def demo_create_orders():
    print('=' * 60)
    print('Create ORDERS')
    print('=' * 60)
    
    # 1
    print('\n1 Limit Order (BID):')
    limit_buy = Order(
        side=OrderSide.BID,
        price=Decimal('100.50'),
        volume=Decimal('100'),
        order_type=OrderType.LIMIT,
        time_in_force=OrderTIF.GTC
    )
    print(f'\t{limit_buy}')
    print(f'\tDATA: {limit_buy.get()}')
    
    # 2
    print('\n2 Limit Order (ASK):')
    limit_sell = Order(
        side=OrderSide.ASK,
        price=Decimal('101.25'),
        volume=Decimal('50'),
        order_type=OrderType.LIMIT,
        time_in_force=OrderTIF.IOC
    )
    print(f'\t{limit_sell}')
    
    # 3
    print('\n3 Market Order (MARKET BUY):')
    market_buy = Order(
        side=OrderSide.BID,
        volume=Decimal('75'),
        order_type=OrderType.MARKET,
        time_in_force=OrderTIF.FOK
    )
    print(f'\t{market_buy}')
    print(f'\tPrice: {market_buy.price} (market order have not price)')
    
    # 4.
    print('\n4 Stop Order (STOP LOSS):')
    stop_order = Order(
        side=OrderSide.ASK,
        price=Decimal('95.00'),
        stop_price=Decimal('96.00'),
        volume=Decimal('100'),
        order_type=OrderType.STOP,
        time_in_force=OrderTIF.GTC
    )
    print(f'\t{stop_order}')
    print(f'\tStop-price: {stop_order.stop_price}')
    
    return [limit_buy, limit_sell, market_buy, stop_order]


def demo_orderbook():
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
    
    print(ob)


def main():
    if not IMPORT_SUCCESS:
        print('FAILED to import modules (((')
        return
    
#    demo_create_orders()
    demo_orderbook()


if __name__ == '__main__':
    main()