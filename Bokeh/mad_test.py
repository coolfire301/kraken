import time
import datetime
import os
import statistics as st
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import krakenex
from pykrakenapi import KrakenAPI
kraken = krakenex.API()
kraken.load_key('kraken.key')
k = KrakenAPI(kraken)

def get_past_10_data(coin_list):
    ohlc, last = k.get_ohlc_data(coin_list + "EUR")
    current_price_list = list(ohlc["close"])[0:20]
    current_time = list(ohlc["time"])[0:20]
    return current_price_list


def calculate_mad(hist_data):
    upper_list = []
    lower_list = []
    data = np.array(hist_data)
    scaled = 1.4826 * (st.mean(abs(data-st.mean(data))))

    upper = st.mean(data) + (scaled * 2)
    lower = st.mean(data) - (scaled * 2)
    return upper, lower




def main():
    data = get_past_10_data("LINK")
    upper_list, lower_list = calculate_mad(data)

    print(upper_list)
    print(lower_list)





main()