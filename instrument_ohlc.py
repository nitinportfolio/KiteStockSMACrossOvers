from kiteconnect import KiteTicker, KiteConnect

import datetime as dt
import sys
import pandas as pd
import os
import time
import numpy as np
import pandas_ta as ta
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)


def instrumentLookup(instrument_df, symbol):
    """Looks up instrument token for a given script from instrument dump"""
    try:
        return instrument_df[instrument_df.tradingsymbol == symbol].instrument_token.values[0]
    except:
        return -1


def fetchOHLC(ticker, interval, duration):
    """extracts historical data and outputs in the form of dataframe"""
    instrument = instrumentLookup(instrument_df, ticker)
    data = pd.DataFrame(
        kite.historical_data(instrument, dt.date.today() - dt.timedelta(duration), dt.date.today(), interval))
    data.set_index("date", inplace=True)
    return data
