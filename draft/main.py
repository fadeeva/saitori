import asyncio
import itertools as it
import os
import random
import time


async def makeitem(size: int = 5) -> str:
    return os.urandom(size).hex()


async def randsleep(caller=None) -> None:
    i = random.randint(0, 10)
    if caller:
        print(f'{caller} sleeping for {i} seconds.')
    await asyncio.sleep(i)

    
async def buy(name: int, q: asyncio.Queue) -> None:
    n = random.randint(0, 10)
    for _ in it.repeat(None, n):  # Synchronous loop for each single buyers
        await randsleep(caller=f'Buyer {name}')
        i = await makeitem()
        t = time.perf_counter()
        await q.put((i, t))
        print(f'Buyer {name} added <{i}> to queue.')

        
async def sell(name: int, q: asyncio.Queue) -> None:
    while True:
        await randsleep(caller=f'Seller {name}')
        i, t = await q.get()
        now = time.perf_counter()
        print(f'Seller {name} got element <{i}>'
              f' in {now-t:0.5f} seconds.')
        q.task_done()

        
async def main(nbuy: int, nsell: int):
    q = asyncio.Queue()
    buyers = [asyncio.create_task(buy(n, q)) for n in range(nbuy)]
    sellers = [asyncio.create_task(sell(n, q)) for n in range(nsell)]
    await asyncio.gather(*buyers)
    await q.join()  # Implicitly awaits sellers, too
    for c in sellers:
        c.cancel()

        
if __name__ == '__main__':
    import argparse
    random.seed(444)
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--nbuy', type=int, default=5)
    parser.add_argument('-s', '--nsell', type=int, default=10)
    ns = parser.parse_args()
    start = time.perf_counter()
    asyncio.run(main(**ns.__dict__))
    elapsed = time.perf_counter() - start
    print(f'Program completed in {elapsed:0.5f} seconds.')
    
    