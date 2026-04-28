import pytest
from datetime import datetime

from src.order import *
from src.exchange import *


def test_exchange_creation():
    exchange = Exchange()
    
    assert exchange.status() is True
