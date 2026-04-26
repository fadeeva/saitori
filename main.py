from decimal import Decimal

try:
    from src.order import Order, OrderStatus, OrderType, OrderSide, OrderTIF, OrderErrorMessages
    from src.orderbook.limit_orderbook import LimitOrderBook
    from src.orderbook.stop_orderbook import StopOrderBook
    from src.orderlogger import *
    
    
    IMPORT_SUCCESS = True
except ImportError as e:
    print(f'Import Error: {e}.')
    IMPORT_SUCCESS = False
    
logger = OrderLogger()

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
        time_in_force=OrderTIF.GTC,
        logger=logger
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
        time_in_force=OrderTIF.IOC,
        logger=logger
    )
    print(f'\t{limit_sell}')
    
    # 3
    print('\n3 Market Order (MARKET BUY):')
    market_buy = Order(
        side=OrderSide.BID,
        volume=Decimal('75'),
        order_type=OrderType.MARKET,
        time_in_force=OrderTIF.FOK,
        logger=logger
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
        time_in_force=OrderTIF.GTC,
        logger=logger
    )
    print(f'\t{stop_order}')
    print(f'\tStop-price: {stop_order.stop_price}')
    
    return [limit_buy, limit_sell, market_buy, stop_order]


def demo_orderbook():
    ob = LimitOrderBook()
    
    orders = [
        (OrderSide.ASK, Decimal('100.00'), Decimal(30)),
        (OrderSide.ASK, Decimal('100.00'), Decimal(20)),
        (OrderSide.ASK, Decimal('100.00'), Decimal(20)),
        (OrderSide.ASK, Decimal('100.00'), Decimal(20)),
        (OrderSide.ASK, Decimal('100.00'), Decimal(20)),
        
#        (OrderSide.BID, Decimal('120.00'), Decimal(50)),
#        (OrderSide.BID, Decimal('120.00'), Decimal(30)),
#        (OrderSide.BID, Decimal('120.00'), Decimal(20)),
#        (OrderSide.BID, Decimal('110.00'), Decimal(50)),
#        (OrderSide.BID, Decimal('110.00'), Decimal(30)),
#        (OrderSide.BID, Decimal('100.00'), Decimal(20)),
    ]
    
    ob = StopOrderBook()
    
    for i in range(5):
        ob.add_to_storage(
            Order(
                side=OrderSide.ASK,
                stop_price=Decimal('100.00') if i%2 else Decimal('120.00'),
                price=Decimal('100.00') if i%2 else Decimal('120.00'),
                volume=Decimal('20'),
                order_type=OrderType.STOP,
                time_in_force=OrderTIF.GTC,
                logger=logger
            )
        )
    
    for i in range(5):
        ob.add_to_storage(
            Order(
                side=OrderSide.BID,
                stop_price=Decimal('120.00') if i%2 else Decimal('100.00'),
                price=Decimal('120.00') if i%2 else Decimal('100.00'),
                volume=Decimal('20'),
                order_type=OrderType.STOP,
                time_in_force=OrderTIF.GTC,
                logger=logger
            )
        )
        
    print(ob.storage_len)
    print(*ob.ask_storage._orders, sep='\n')
    print(*ob.bid_storage._orders, sep='\n')
    unexec = ob.get_activated(Decimal('100.00'))
    print(ob.storage_len)
    print(*ob.ask_storage._orders, sep='\n')
    print(*ob.bid_storage._orders, sep='\n')
    print(unexec)
    
    
def main():
    if not IMPORT_SUCCESS:
        print('FAILED to import modules (((')
        return
    
#    demo_create_orders()
    demo_orderbook()


if __name__ == '__main__':
    main()