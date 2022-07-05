# -*- coding: utf-8 -*-
"""
Created on Sun May 22 14:37:15 2022

@author: ziongh
"""

import random
import asyncio
import os
import logging
import datetime
import tweepy
import pandas as pd
import json


def main():
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()

    try:
        loop.create_task(consume())
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Process interrupted by the user")
    finally:
        logging.info("Finishing process")
        loop.close()


if "__main__" == __name__:
    pass
