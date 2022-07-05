# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 12:05:49 2022

@author: ziongh
"""

import asyncio
#from collections import coroutines as ccor
from collections.abc import Awaitable
from random import randint
from dataclasses import dataclass



@dataclass
class AsyncRandom(Awaitable):
    xmin: int
    xmax:int

    def __await__(self):
        return (self.randint().__await__())

    async def randint(self):
        value = randint(self.xmin, self.xmax)
        return await asyncio.sleep(0.2, result=value)


async def generate_random(xmin, xmax):
    await randint(xmin, xmax)


async def main(xmin=0, xmax=10):
    random = AsyncRandom(xmin, xmax)
    counter = 0
    while True:
        print(await random)
        counter = counter + 1

        if counter>10:
            break



if "__main__" == __name__:
    asyncio.run(main())