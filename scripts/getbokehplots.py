
# coding: utf-8

# Standard packages
import numpy as np
import pandas as pd
import os.path as path
import datetime as dt
import warnings
import sys

from bokeh.plotting import figure, show, save, output_file, output_notebook
from bokeh.palettes import Spectral11, colorblind, Inferno, BuGn, brewer
from bokeh.models import HoverTool, value, LabelSet, Legend, ColumnDataSource,LinearColorMapper,BasicTicker, PrintfTickFormatter, ColorBar
from bokeh.palettes import Spectral3
import bokeh.palettes
from bokeh.embed import components
from bokeh.layouts import gridplot
from bokeh.models import Range1d


# CRNS IDs to be processed
ids = eval(sys.argv[1])
# Data root dir
datadir = sys.argv[2]
# Target for bokeh html file
htmlfile = sys.argv[3]

plot_width = 550

# Read data
crns = {}
for id in ids:
    df = pd.read_csv(path.join(datadir, "%d/%d_CRNS.txt" % (id, id)), sep="\t")
    df.datetime = pd.to_datetime(df.datetime)
    df = df.set_index("datetime")
    print(id, end=": ")
    print("%s to %s" % (df.index[0], df.index[-1]) )
    df = df[:"2019-07-23 00:00:00"]
    crns[id] = df

min_dtime = np.min([crns[key].index[0] for key in crns.keys()])
max_dtime = np.max([crns[key].index[-1] for key in crns.keys()])

# In[119]:

TOOLS = 'save,pan,box_zoom,reset,wheel_zoom,hover'
colors=bokeh.palettes.Category20_20#bokeh.palettes.Set3_12 + bokeh.palettes.Set2_6

plts = []

p = figure(title="Raw (moderated) neutron counts, all probes", x_axis_type='datetime',
           y_axis_type="linear", plot_height = 430,
           tools = TOOLS, plot_width = plot_width)
p.xaxis.axis_label = 'Datetime'
p.yaxis.axis_label = 'Raw neutron counts'
for i, id in enumerate(ids):
    p.circle(crns[id].index, crns[id].counts1, line_color=colors[i], fill_color=colors[i], fill_alpha=0.9,
             size=2, legend=str(id))
p.x_range=Range1d(min_dtime, max_dtime)
p.y_range=Range1d(0, 2000)
p.legend.location = "center_left"
p.legend.spacing = 1
#p.legend.label_text_font_size = "8px"
p.legend.background_fill_alpha = 0.5

plts.append(p)

p = figure(title="Battery voltage, all probes", x_axis_type='datetime',
           y_axis_type="linear", plot_height = 430,
           tools = TOOLS, plot_width = plot_width)
p.xaxis.axis_label = 'Datetime'
p.yaxis.axis_label = 'Voltage (V)'
for i, id in enumerate(ids):
    p.circle(crns[id].index, crns[id].volt, line_color=colors[i], fill_color=colors[i], fill_alpha=0.9,
             size=2, legend=str(id))
p.x_range=Range1d(min_dtime, max_dtime)
p.y_range=Range1d(11, 15)
p.legend.location = "center_left"
p.legend.spacing = 1
p.legend.background_fill_alpha = 0.5

plts.append(p)


for i, id in enumerate(ids):
    p = figure(title="Raw (moderated) neutron counts, CRNS #%d" % id, x_axis_type='datetime',
               y_axis_type="linear", plot_height = 200, plot_width = plot_width,
               tools = TOOLS)
    p.xaxis.axis_label = 'Datetime'
    p.yaxis.axis_label = 'Counts (-)'
    p.circle(crns[id].index, crns[id].counts1, size=2)
    p.x_range=Range1d(min_dtime, max_dtime)
    #p.legend.location = "center_left"
    plts.append(p)


grid = gridplot(plts, merge_tools=False, ncols=1)

output_file(htmlfile, title="Time series of raw neutron counts")
save(grid)
#script, div = components(p)


# Add correct header to html
f = open(htmlfile, "r")
html = f.read()
f.close()
html = html.strip()
replacement = '''<html>
<div class="blurb">
	<h1>JFC Fendt: Instrument monitor</h1>
</div><!-- /.blurb -->
'''
html = html.replace('<html lang="en">', replacement)
f = open(htmlfile, "w")
f.write("---\nlayout: default\ntitle: cosmic pages\n---\n")
f.write(html)
f.close()
