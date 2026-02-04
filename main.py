from decimal import Decimal

try:
    from src.order import Order, OrderStatus, OrderType, OrderSide, OrderTIF, OrderErrorMessages
    IMPORT_SUCCESS = True
except ImportError as e:
    print(f'Import Error: {e}.')
    IMPORT_SUCCESS = False
    
    
def main():
    if not IMPORT_SUCCESS:
        print('FAILED to import modules (((')


if __name__ == '__main__':
    main()