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


def get_wallet():
    balance = (kraken.query_private('Balance')["result"])
    euro = balance["ZEUR"]
    return euro

def create_coin_list():
    coin_list = ["CRV"]
    return coin_list

def get_past_10_data(coin_list):
    ohlc, last = k.get_ohlc_data(coin_list + "EUR")
    current_price_list = list(ohlc["close"])[0:20]
    current_time = list(ohlc["time"])[0:20]
    return current_price_list, current_time

def calculate_mad(hist_data):
    upper_list = []
    lower_list = []
    for x in range(1, 11):
        data = np.array(hist_data[x:x+10])
        scaled = 1.4826 * (st.mean(abs(data-st.mean(data))))
        upper = st.mean(data) + (scaled * 2)
        lower = st.mean(data) - (scaled * 2)
        upper_list.append(upper)
        lower_list.append(lower)
    return upper_list, lower_list

def calculate_dip_or_top(hist_data, upper_list, lower_list):
    if hist_data[-1] > upper_list[-1]:
        #print("SELL at" + str(hist_data[-1]))
        return 2
    elif hist_data[-1] < lower_list[-1]:
        #print("BUY at" + str(hist_data[-1]))
        return 1
    else:
        #print("DO nothing")
        return 0

def write_to_file(coin_list, bought, totaal, current_prijs, totale_winst):
    f = open("made_trades.txt", "a")
    line = coin_list + "\t" + str(float(bought) * float(totaal)) + "\t" + str((float(totaal) * float(current_prijs))) + "\t" + str(totale_winst) + "\n"
    f.write(line)
    f.close()

def visualize(hist_data, hist_time, upper_list, lower_list):
    y_as = []
    for x in range(len(hist_time)):
        y_as.append(x)



    plt.plot(y_as, hist_data)
    plt.plot(y_as[20:], upper_list)
    plt.plot(y_as[20:], lower_list)

    #plt.plot(y_axis, hist_data)
   # plt.legend()
    plt.draw()
    #plt.show()
    plt.pause(0.5)
    plt.clf()

def get_current_price(coin_list):
    #print(coin_list)
    coin_data = k.get_ticker_information(coin_list + 'EUR')
    prijs = coin_data.a[0][0]
    return prijs

def buy_coins(coin, volume):
    response = kraken.query_private('AddOrder',
                                    {'pair': coin + '/EUR',
                                     'type': 'buy',
                                     'ordertype': 'market',
                                     'volume': volume})
    return response

def sell_coins(coin):
    response = kraken.query_private('AddOrder',
                                    {'pair': coin + '/EUR',
                                     'type': 'sell',
                                     'ordertype': 'market',
                                     'volume': (kraken.query_private('Balance')["result"])[coin]})
    return response

def get_amount_of_coins_bought(coin_list):
    balance = (kraken.query_private('Balance')["result"])
    amount = balance[coin_list]
    return amount

def main():
    coin_list = ["LINK"]
    #start up
    euro = get_wallet()
    try:
        os.remove("made_trades.txt")
    except:
        pass
    f = open("made_trades.txt", "a")
    line = "Coins" + "\t" + "Buy" + "\t" + "Sell" + "\t" + "Winst" + "\n"
    f.write(line)
    f.close()

    euro_wallet = float(get_wallet())
    print(euro_wallet)
    input()
    bought = [0] * len(coin_list)
    hist_data = [0] * len(coin_list)
    hist_time = [0] * len(coin_list)
    upper_list = [0] * len(coin_list)
    lower_list = [0] * len(coin_list)
    totaal = [0] * len(coin_list)
    for x in range(len(coin_list)):
        hist_data[x], hist_time[x] = get_past_10_data(coin_list[x])
        upper_list[x], lower_list[x] = calculate_mad(hist_data[x])
        time.sleep(2)

        print(hist_data[x])
        print(len(hist_data[x]), len(hist_time[x]))
    i = 0

    a = 0
    while i < 100:
        for x in range(len(coin_list)):
            current_prijs = get_current_price(coin_list[x])
            new_data = hist_data[x][1:]
            new_data.append(float(current_prijs))
            new_time = hist_time[x][1:]
            new_time.append(int(time.time()))
            upper_list[x], lower_list[x] = calculate_mad(new_data)
            buy_or_sell = calculate_dip_or_top(new_data, upper_list[x], lower_list[x])


            #For test purpose

            #bought = [40000]

            #if a == 0:
            #    buy_or_sell = 1
            #else:
            #    buy_or_sell = 2

            if buy_or_sell == 1 and float(bought[x]) == 0:
                current_time = datetime.now().strftime("%H:%M:%S")
                print(coin_list[x], "bought for ", current_prijs, current_time, "\n")
                bought[x] = (current_prijs)
                euro_before = float(get_wallet())
                volume = (euro_wallet - 1) / float(current_prijs)
                response = buy_coins(coin_list[x], volume)
                print("er is totaal:" + str(volume) + " " + coin_list[x] + "\n\n====\n")
                #print(response)
                totaal[x] = get_amount_of_coins_bought(coin_list[x])
                print(totaal[x])
                euro_wallet = float(get_wallet())
                print("er is totaal:" + str(totaal[x]) + " " + coin_list[x] + "\n\n====\n")
            elif buy_or_sell == 2 and float(bought[x]) > 0:
                current_time = datetime.now().strftime("%H:%M:%S")
                print(coin_list[x], "sold for ", current_prijs, current_time)
                response = sell_coins(coin_list[x])
                #print(response)
                euro_wallet = float(get_wallet())
                winst = euro_wallet - euro_before
                print(coin_list[x] + "Sold for" + str(current_prijs) + "Een totale winst van:" + str(winst))
                write_to_file(coin_list[x], bought[x], totaal[x], current_prijs, winst)
                bought[x] = 0
            #visualize(new_data, new_time, upper_list, lower_list)
            time.sleep(60)

            #plt.clf()

            a = 1

main()
