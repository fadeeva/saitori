import time

import numpy as np


sellers = 10_000
buyers = 8_000
amount = 1_000_000

init_price = np.round(np.random.uniform(low=100, high=200), 2)


print('BUY |_____| PRICE |_____| SELL')

print(init_price)