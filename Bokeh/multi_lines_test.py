import numpy as np

from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource, Grid, LinearAxis, MultiLine, Plot
from bokeh.models import DatetimeTickFormatter, Select, TableColumn, DataTable
from datetime import datetime
from bokeh.layouts import layout
from bokeh.plotting import figure
from random import randrange



p = figure(x_axis_type="datetime", width=1200, height = 600)

source = ColumnDataSource(dict(x=[], y=[]))
source2 = ColumnDataSource(dict(x=[], y=[]))
source3 = ColumnDataSource(dict(x=[], y=[]))

p.line(x="x", y="y", source=source, color='green')
p.line(x="x", y="y", source=source2, color='red')
p.line(x="x", y="y", source=source3, color='red')

def x_create_value():
    return (randrange(10))

def y_create_value():
    return (randrange(10))


def update():
    new_data = dict(x=[datetime.now()], y=[y_create_value()])
    new_data2 = dict(x=[datetime.now()], y=[y_create_value()])
    new_data3 = dict(x=[datetime.now()], y=[y_create_value()])
    source.stream(new_data, rollover=20)
    source2.stream(new_data2, rollover=20)
    source3.stream(new_data3, rollover=20)
    print(new_data)


def update_intermed(attrname, old, new):
    source.data = dict(x=[], y=[])
    source2.data = dict(x=[], y=[])
    source3.data = dict(x=[], y=[])
    update()

#xaxis = LinearAxis()
#p.add_layout(xaxis, 'below')

#yaxis = LinearAxis()
#p.add_layout(yaxis, 'left')

#p.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
#p.add_layout(Grid(dimension=1, ticker=yaxis.ticker))



#config layouy
lay_out = layout([[p]])

curdoc().title = "Streaming stock data example"
curdoc().add_root(lay_out)
curdoc().add_periodic_callback(update, 1000)