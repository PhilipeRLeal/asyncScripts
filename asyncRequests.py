# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:21:16 2022

This script demonstrate how to convert a sync request into async,
without changing packages. An aiohttp version is also provided.

The examples below retrieves several requests (pokemon information)
from a default url. Each request is a pokemon.

The resultant objects are pandas.dataframes with the
respective responses (pokemons' info).

This example was retrieved by: https://www.youtube.com/watch?v=GpqAQxH1Afc

@author: Philipe Riskalla Leal
"""
from collections import namedtuple
import asyncio
import timeit
#from collections import coroutines as ccor
from collections.abc import Awaitable
from dataclasses import dataclass, field
import requests
import aiohttp
import pandas as pd
from abc import ABC, abstractmethod

# How to transform a synchronous request into async using requests
@dataclass
class Requester(Awaitable, ABC):
    pokemons: set = field(default_factory=set)

    def responseToNamedTuple(self, pokemon) -> tuple:
        """Converts a response (pokemon) dictionary into
        a hashable (namedtuple) object

        Parameters
        ----------
        pokemon : response object (aiohttp or requests response object)

        Returns
        -------
        tuple
            hashable version of the response.

        """

        HashablePokemon = namedtuple("Pokemon", "id name")
        HashablePokemon = HashablePokemon(pokemon["id"],
                                          pokemon["name"])

        return HashablePokemon



    def __await__(self):
        return (self.send_async_request().__await__())

    @abstractmethod
    async def send_async_request(self,
                                 url: str,
                                 verbose: bool=False) -> int:
        return int

    def send_request(self, url: str, verbose:bool=False) -> int:
        if verbose:
            print("Sending HTTP request")
        response = requests.get(url)

        # A set must be formed of hashable instances.
        # so, lets convert the response into a
        # hashable object (e.g., namedtuple)
        hashablePokemon = self.responseToNamedTuple(response.json())

        # now we can finally add it to the set
        self.pokemons.add(hashablePokemon)
        return response.status_code

@dataclass
class AsyncRequests(Requester):
    pokemons: set = field(default_factory=set)

    async def send_async_request(self,
                                 url: str,
                                 verbose: bool=False) -> int:
        """Sends requests (using requests library) asynchronously.

            Parameters
            ----------
            url : str
                the url that will be fetched.

            Returns
            -------
            int
                the response value of the server.

            """
        return await asyncio.to_thread(self.send_request, url, verbose)


@dataclass
class AsyncAioHTTPRequests(Requester):

    async def send_async_request(self,
                                 url: str,
                                 verbose: bool=False) -> int:
        """Sends requests (using requests library) asynchronously.

            Parameters
            ----------
            url : str
                the url that will be fetched.

            Returns
            -------
            int
                the response value of the server.

        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                responseJson = await response.json()
                # A set must be formed of hashable instances.
                # so, lets convert the response into a
                # hashable object (e.g., namedtuple)
                hashablePokemon = self.responseToNamedTuple(responseJson)

                # now we can finally add it to the set
                self.pokemons.add(hashablePokemon)

                return response.status

def fetchPokemonsFromRequester(requester:Requester) -> pd.DataFrame:
    index = pd.Index([x.id for x in requester.pokemons],
                     name="Pokemon ID"
                     )
    df = pd.Series([x.name for x in requester.pokemons],
                   index=index,
                   name="Pokemon Name")

    return df


async def asyncRequests(requester: Requester,
                        n: int=150,
                        verbose: bool=False) -> Requester:

    for pokemon_id in range(1, n):
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        status_code = await asyncio.gather(
            requester.send_async_request(url, verbose))

    return requester



def syncRequests(requester: Requester,
                  n: int=150,
                  verbose: bool=False)  -> Requester:

    for pokemon_id in range(1, n):
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        requester.send_request(url, verbose)

    return requester

async def main(n: int=20, repeats: int=3,
               returnValues: bool=False,
               verbose: bool=False
               ) -> None:

    print("N° of repeats: ", repeats)

    print("Starting sync requests: ")
    # First the sync method (as a base reference):
    syncTime = min(timeit.repeat(lambda : syncRequests(AsyncRequests(),
                                                       n,
                                                       verbose),
                                             number=repeats
                                             )
                              )
    print(f"Time taken for running synchronously: {syncTime}")

    # then the requests async version:
    print("Starting Requests async method: ")
    requestAsyncTime = min(timeit.repeat(lambda : asyncRequests(AsyncRequests(),
                                                                n,
                                                                verbose),
                                                    number=repeats
                                                    )
                                       )
    print(f"Time taken for running requests asynchronously: {requestAsyncTime}")


    # then the aiohttp async version:
    print("Starting aiohttp async method: ")
    aioHTTPAsyncTime = min(timeit.repeat(lambda : asyncRequests(AsyncAioHTTPRequests(),
                                                                n,
                                                                verbose),
                                                    number=repeats
                                                    )
                                     )
    print(f"Time taken for running async with aiohttp: {aioHTTPAsyncTime}")


    print("Speed up ratio: (syncTime/requestAsyncTime) {0}".format(
            (syncTime)/(requestAsyncTime) )
         )


    print("Speed up ratio: (syncTime/AioHTTPAsync) {0}".format(
            (syncTime)/(aioHTTPAsyncTime) )
         )

    ##################################################################


    if returnValues:
        requester = asyncRequests(AsyncRequests(),n,verbose)
        df = fetchPokemonsFromRequester(requester)

        print(df)

        print("Requests DF: \n", df)

    return requester, aioRequester



if "__main__" == __name__:
    requester, aioRequester = asyncio.run(main())