
# coding: utf-8

# # Comparing multiple CRNS probes

# **For the time being, this notebook is a sandbox.** Step by step, we will migrate mature functions to the actual `cosmicsense` library.
#
# For a detailed explanation of prepprocessing steps, please refer to [from_n_to_theta.ipynb](https://cosmicsense.readthedocs.io/en/latest/notebooks/n_to_theta.html).

# In[30]:


# Standard packages
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as colors
import matplotlib as mpl
import numpy as np
import pandas as pd
import os.path as path
import datetime as dt
import warnings

from bokeh.plotting import figure, show, save, output_file, output_notebook
from bokeh.palettes import Spectral11, colorblind, Inferno, BuGn, brewer
from bokeh.models import HoverTool, value, LabelSet, Legend, ColumnDataSource,LinearColorMapper,BasicTicker, PrintfTickFormatter, ColorBar
from bokeh.palettes import Spectral3
import bokeh.palettes
from bokeh.embed import components
from bokeh.layouts import gridplot
from bokeh.models import Range1d

import cosmicsense as cs


warnings.simplefilter('once', RuntimeWarning)

ids = [1, 2, 3, 4, 5, 6, 7, 8, 14, 16, 17, 18, 19, 21, 22, 23, 24, 25]

#fpath = "/home/maik/b2drop/cosmicsense/inbox/fendt/timeseries/crns/JFC-1/"
fpath = "/media/x/cosmicsense/data/fendt/crns/"
htmlfile_merge = "/media/x/cosmicsense/git/misc/fendt/merged_crns.html"
plot_width = 550


crns = {}
for id in ids:
    df = pd.read_csv(path.join(fpath, "%d/%d_CRNS_merge.txt" % (id, id)), sep="\t")
    df.datetime = pd.to_datetime(df.datetime)
    df = df.set_index("datetime")
    if id==4:
        df["cph1"] = (df.counts1 + df.counts2) / cs.conv.s_to_h(df.nsecs1)
    else:
        df["cph1"] = df.counts1 / cs.conv.s_to_h(df.nsecs1)
        try:
            df["cph2"] = df.counts2 / cs.conv.s_to_h(df.nsecs2)
        except AttributeError:
            pass
    print(id, end=": ")
    print("%s to %s" % (df.index[0], df.index[-1]) )
    # truncate end of campaign
    df = df[:"2019-07-23 00:00:00"]
    crns[id] = df


# In[35]:


min_dtime = np.min([crns[key].index[0] for key in crns.keys()])
max_dtime = np.max([crns[key].index[-1] for key in crns.keys()])


pars =  {
    1: {"mincph": 500, "maxcph": 1000, "mininterv": -9999, "type": "CRS 2000-B, Scn.", "lut": "forest/meadow"},
    2: {"mincph": 500, "maxcph": 1100, "mininterv": -9999, "type": "CRS 1000", "lut": "meadow"},
    3: {"mincph": 500, "maxcph": 1100, "mininterv": -9999, "type": "CRS 1000", "lut": "meadow"},
    4: {"mincph": 6000, "maxcph": 9500, "mininterv": -9999, "type": "Lab C", "lut": "meadow"},
    5: {"mincph": 800, "maxcph": 1500, "mininterv": -9999, "type": "CRS 1000-B", "lut": "meadow"},
    6: {"mincph": 800, "maxcph": 1500, "mininterv": -9999, "type": "CRS 1000-B", "lut": "meadow, forest close"},
    7: {"mincph": 1000, "maxcph": 1700, "mininterv": -9999, "type": "CRS 1000-B", "lut": "meadow"},
    8: {"mincph": 1300, "maxcph": 2500, "mininterv": -9999, "type": "CRS 2000-B", "lut": "meadow"},
    14: {"mincph": 800, "maxcph": 1500, "mininterv": -9999, "type": "CRS 2000", "lut": "forest"},
    16: {"mincph": 1500, "maxcph": 2500, "mininterv": -9999, "type": "CRS 2000-B", "lut": "meadow"},
    17: {"mincph": 1400, "maxcph": 2400, "mininterv": -9999, "type": "CRS 2000-B", "lut": "meadow"},
    18: {"mincph": 500, "maxcph": 1000, "mininterv": -9999, "type": "CRS 1000", "lut": "meadow"},
    19: {"mincph": 1300, "maxcph": 2300, "mininterv": -9999, "type": "CRS 2000-B", "lut": "forest"},
    21: {"mincph": 1400, "maxcph": 2300, "mininterv": -9999, "type": "CRS 2000-B", "lut": "meadow, forest close"},
    22: {"mincph": 1100, "maxcph": 2100, "mininterv": -9999, "type": "CRS 2000-B", "lut": "forest"},
    23: {"mincph": 1200, "maxcph": 2200, "mininterv": -9999, "type": "CRS 2000-B", "lut": "meadow, peat"},
    24: {"mincph": 1600, "maxcph": 2600, "mininterv": -9999, "type": "CRS 2000-B", "lut": "meadow"},
    25: {"mincph": 900, "maxcph": 1500, "mininterv": -9999, "type": "CRS 1000-B", "lut": "meadow"},

}

buffer = 0.075

for i, key in enumerate(crns.keys()):
    x = crns[key].cph1.copy()
    if not key==1:
        x[x > pars[key]["maxcph"]] = np.nan
    x[x < pars[key]["mincph"]] = np.nan
    x[crns[key].nsecs1 < pars[key]["mininterv"]] = np.nan
    median24 = x.resample("24H").median()
    # Maxfilter
    max6 = x.resample("6H").max()
    median24max6 = max6.resample("24H").median()
    maxfilter = np.array(median24max6 + buffer * median24)
    # Minfilter
    min6 = x.resample("6H").min()
    median24min6 = min6.resample("24H").median()
    minfilter = np.array(median24min6 - buffer * median24)
    # Resample filter to original time stamps
    crns[key]["cph1_maxfilter"] = np.interp(x.index, median24.index, maxfilter)
    crns[key]["cph1_minfilter"] = np.interp(x.index, median24.index, minfilter)
    # Fill gaps
    crns[key]["cph1_maxfilter"] = crns[key].cph1_maxfilter.interpolate()
    crns[key]["cph1_minfilter"] = crns[key].cph1_minfilter.interpolate()
    # Apply filter
    crns[key]["cph1_filtered"] = x
    if not key==1:
        crns[key].loc[crns[key].cph1 > crns[key].cph1_maxfilter, "cph1_filtered"] = np.nan
        crns[key].loc[crns[key].cph1 < crns[key].cph1_minfilter, "cph1_filtered"] = np.nan


dtrange6 = pd.date_range('2019-05-01 00:00:00', max_dtime, freq="6H")
dtrange24 = pd.date_range('2019-05-01 00:00:00', max_dtime, freq="24H")
crns6h = pd.DataFrame({}, index=dtrange6)
crns24h = pd.DataFrame({}, index=dtrange24)

for i, key in enumerate(crns.keys()):
    crns6h = pd.merge(crns6h, crns[key].cph1_filtered.resample("6H").mean(),
                      how="left", left_index=True, right_index=True)
    crns6h[key] = crns6h.cph1_filtered
    crns6h = crns6h.drop("cph1_filtered", axis=1)
    # 24 h
    crns24h = pd.merge(crns24h, crns[key].cph1_filtered.resample("24H").mean(),
                      how="left", left_index=True, right_index=True)
    crns24h[key] = crns24h.cph1_filtered
    crns24h = crns24h.drop("cph1_filtered", axis=1)


# In[40]:



TOOLS = 'save,pan,box_zoom,reset,wheel_zoom,hover'
colors=bokeh.palettes.Category20_20#bokeh.palettes.Set3_12 + bokeh.palettes.Set2_6

from bokeh.models import Span
from bokeh.models import Label

plts = []

for i, id in enumerate(ids):
    p = figure(title="Counts/hour (moder.), #%d (%s, %s)" % (id, pars[id]["type"], pars[id]["lut"]), x_axis_type='datetime',
               y_axis_type="linear", plot_height = 200, plot_width = plot_width,
               tools = TOOLS)
    if id==1:
        vline = Span(location=dt.datetime(2019,6,6,8,0,0), dimension='height', line_color='red', line_width=1, line_dash=[2])
        p.renderers.extend([vline])
        mytext = Label(x=dt.datetime(2019,6,6,8,0,0), y=1200, text='Shield rem.',
                       text_align="right", text_font_size="9pt")
        p.add_layout(mytext)
    p.xaxis.axis_label = 'Datetime'
    p.yaxis.axis_label = 'Counts per hour'
    p.circle(crns[id].index, crns[id].cph1_filtered, size=1, color="lightgrey", legend="20 mins")
    p.line(crns6h.index+dt.timedelta(hours=3), crns6h[id], line_color="black", line_width=2, legend="6 hours")
    p.line(crns24h.index+dt.timedelta(hours=12), crns24h[id], line_color="green", line_dash=[2], line_width=2, legend="24 hours")
    p.x_range=Range1d(min_dtime, max_dtime)
    miny, maxy = None, None
    if pars[id]["type"]=="CRS 2000-B":
        miny, maxy = 1400, 2400
    if pars[id]["type"]=="CRS 1000":
        miny, maxy = 500, 1000
    if pars[id]["type"]=="CRS 1000-B":
        miny, maxy = 900, 1500
    if pars[id]["type"]=="CRS 2000":
        miny, maxy = 1000, 1400
    if miny is not None:
        p.y_range=Range1d(miny, maxy)
    p.legend.location = "center_left"
    p.legend.background_fill_alpha = 0.6
    #p.legend.location = "center_left"
    plts.append(p)


grid = gridplot(plts, merge_tools=False, ncols=1)

output_file(htmlfile_merge, title="Time series of counts per hour")
save(grid)

# Add correct header to html
f = open(htmlfile_merge, "r")
html = f.read()
f.close()
html = html.strip()
replacement = '''<html>
<div class="blurb">
	<h1>JFC Fendt: Processed neutron counts  </h1>
</div><!-- /.blurb -->
<p> Data merged from SD and telemetry...counts per hour...filtered...resampled.
'''
html = html.replace('<html lang="en">', replacement)
f = open(htmlfile_merge, "w")
f.write("---\nlayout: default\ntitle: cosmic pages\n---\n")
f.write(html)
f.close()
