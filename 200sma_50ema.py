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
from instrument_ohlc import instrumentLookup, fetchOHLC

access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

instrument_dump = kite.instruments("NSE")
instrument_df = pd.DataFrame(instrument_dump)




instrument_dump_nfo = kite.instruments("NFO")
instrument_df_nfo = pd.DataFrame(instrument_dump_nfo)
fno=instrument_df_nfo["name"].unique()


def crossover_200S_50E_wk(ticker):
    data = fetchOHLC(ticker, "day", 2000)
    ohlc_dict = {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }

    data1 = data.resample('W').agg(ohlc_dict)
    # print(data1)
    # pd.concat([data,data1], axis=0, join='inner')
    # data1 = data1.copy()
    data1["Entity Name"] = ticker
    data1["ema_50_w"] = ta.ema(data1["close"], length=50)
    data1["sma_200_w"] = ta.sma(data1["close"], length=200)
    data2 = data1[-1:]
    if ((data2["open"][-1] <= data2["ema_50_w"][-1]) and (data2["ema_50_w"][-1] <= data2["close"][-1])) or (
            (data2["open"][-1] >= data2["ema_50_w"][-1]) and (data2["ema_50_w"][-1] >= data2["close"][-1])):
        return(data2["Entity Name"][-1] + " - 50 EMA cross-over")
    elif ((data2["open"][-1] <= data2["sma_200_w"][-1]) and (data2["sma_200_w"][-1] <= data2["close"][-1])) or (
            (data2["open"][-1] >= data2["sma_200_w"][-1]) and (data2["sma_200_w"][-1] >= data2["close"][-1])):
        # data2["close"][-1]==data2["sma_200_w"][-1]:
        return(data2["Entity Name"][-1] + " - 200 SMA cross-over")
    # else:
    #    print()
    # print("No cross-over for - "+data2["Entity Name"][-1])

    #return (ticker, data2["close"][-1], data2["ema_50_w"][-1], data2["sma_200_w"][-1])

output = ""
for fnostk in fno.tolist():

    if fnostk not in ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY", "IRCTC", "SBICARD"]:
        if crossover_200S_50E_wk(fnostk) is not None:
        #crossover_200S_50E_wk(fnostk)

            output = output + (crossover_200S_50E_wk(fnostk)+"\n")
print(output)




#print(config.sections())
#print(config["KITE-API"])
#print(list(config["KITE-API"]))
#print(config["KITE-API"]["cwd"])
#print(config["KITE-API"]["access_token"])
#print(config["KITE-API"]["key_secret"])


#kite = KiteConnect(api_key=key_secret[0])
#kite.set_access_token(access_token)
