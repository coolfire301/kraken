from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, Select, TableColumn, DataTable
from bokeh.layouts import layout
from bokeh.plotting import figure
from bokeh.models import Div
from datetime import datetime
import pandas as pd
import numpy as np
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



#create figure
p = figure(x_axis_type="datetime", width=1200, height = 600)


ohlc, last = k.get_ohlc_data("LINK" + "EUR")
current_price_list = list(ohlc["close"])[0:20]
past_data = current_price_list

# generate data
def create_value():
        coin_data = k.get_ticker_information('LINK'+ 'EUR')
        prijs = coin_data.a[0][0]
        time.sleep(2)
        return prijs


def calculate_upper_and_lower():
    global past_data
    data = np.array(past_data)
    scaled = 1.4826 * (st.mean(abs(data - st.mean(data))))
    upper = st.mean(data) + (scaled * 2)
    lower = st.mean(data) - (scaled * 2)
    past_data.append(float(current_price()))
    past_data = past_data[1:]
    return upper, lower



def get_wallet():
    balance = (kraken.query_private('Balance')["result"])
    euro = balance["ZEUR"]
    return str(euro)


def current_price():
    coin_data = k.get_ticker_information('LINK'+ 'EUR')
    prijs = coin_data.a[0][0]
    time.sleep(1)
    return prijs



# create data source
source = ColumnDataSource(dict(x=[], y=[]))

source_upper = ColumnDataSource(dict(x=[], y=[]))

source_lower = ColumnDataSource(dict(x=[], y=[]))

hist_data = []

#upper_line = p.line(x="x", y=0, source=source, color='blue')
#p.line(x="x", y="y", source=source, color='firebrick')
#p.circle(x="x", y="y", color = "firebrick", source=source)
#p.line(x="x", y=calculate_lower(), source=source, color='blue')
p.line(x="x", y="y", source=source_upper, color='firebrick')
p.line(x="x", y="y", source=source, color='green')
p.line(x="x", y="y", source=source_lower, color='firebrick')

div = Div(text="""Current Value:""", width=400, height=40, style={'font-size': '300%', 'color': 'black'})
div2 = Div(text=current_price(), width=200, height=10, style={'font-size': '300%', 'color': 'black', 'width' : '600px',  'margin': '0 auto'})

div4 = Div(text="""""", width=200, height=100)

div3 = Div(text="""Wallet is:""", width=200, height=10, style={'font-size': '200%', 'color': 'black'})

div5 = Div(text=get_wallet(), width=160, height=10, style={'font-size': '200%', 'color': 'black'})

div6 = Div(text="""BUYING.....""", width=200, height=100, style={'font-size': '200%', 'color': 'black'})

div8 = Div(text="""BOUHGT FOR: 14,60""", width=1000, height=100, style={'font-size': '200%', 'color': 'black'})

div7 = Div(text="""Recent trades""", width=200, height=10, style={'font-size': '200%', 'color': 'black'})

div9 = Div(text="""Totale winst:""", width=400, height=20, style={'font-size': '300%', 'color': 'black'})

div10 = Div(text="""2 euro""", width=400, height=20, style={'font-size': '300%', 'color': 'black'})

opvulling1 = Div(text="""""", width=200, height=100)
opvulling2 = Div(text="""""", width=70, height=100)
opvulling3 = Div(text="""""", width=110, height=100)
opvulling4 = Div(text="""""", width=50, height=100)

df = pd.DataFrame({
    'COIN': ['Positive', 'Negative', 'Negative'],
    'BUY': ['Negative', 'Negative', 'Negative'],
    'SELL': ['Negative', 'Invalid', 'Positive'],
    'WINST': ['Positive', 'Negative', 'Negative'],
    'GOOD': ['Positive', 'Positive', 'Negative']
})

sc = ColumnDataSource(df)

columns = [
    TableColumn(field='COIN', title='COIN'),
    TableColumn(field='BUY', title='BUY'),
    TableColumn(field='SELL', title='SELL'),
    TableColumn(field='WINST', title='WINST'),
    TableColumn(field='GOOD', title='GOOD')
]

myTable = DataTable(source=sc, columns=columns)

#create periodic callback function

def update():
       #get price
       price = create_value()
       #Load price data to graph
       new_data = dict(x=[datetime.now()], y=[float(price)])
       source.stream(new_data, rollover=20)

       #Load upper and lower data to graph
       upper, lower = calculate_upper_and_lower()
       upper_data= dict(x=[datetime.now()], y=[upper])
       lower_data = dict(x=[datetime.now()], y=[lower])
       source_upper.stream(upper_data, rollover=20)
       source_lower.stream(lower_data, rollover=20)

       div2.text = price
       div5.text = get_wallet()
       p.title.text="LINK value"
       buy_or_sell = 1
       if div6.text == "BUYING....." and buy_or_sell == 1:
           div8.text = "BOUGHT FOR:"
           div6.text = "SELLING....."
       elif div6.text == "SELLING....." and buy_or_sell == 2:
           div6.text = "SELLING....."


def update_intermed(attrname, old, new):
       source.data = dict(x=[], y=[])
       source_upper = dict(x=[], y=[])
       source_lower = dict(x=[], y=[])
       update()

data_pattern = ["%Y-%m-%d\n%H:%M:%S"]

p.axis.formatter = DatetimeTickFormatter(
       seconds = data_pattern,
       minsec = data_pattern,
       minutes = data_pattern,
       hours = data_pattern,
       days = data_pattern,
       months = data_pattern,
       years = data_pattern
)

#p.xaxis.major_label_orientation=radians(80)
p.xaxis.axis_label = "Date"
p.yaxis.axis_label = "Value"



#config layouy
#lay_out = layout([[p], [select]])
lay_out = layout([
    [p, [opvulling1, div, [opvulling2, div2, div9], [opvulling1,opvulling3, div10], opvulling1, [opvulling1, div6]]],
    [div7],[opvulling1],
    [myTable, div4, div3, div5, opvulling4, div8]
])

curdoc().title = "Streaming stock data example"
curdoc().add_root(lay_out)
curdoc().add_periodic_callback(update, 1000)





















