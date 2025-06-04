#!/usr/bin/env python
# coding: utf-8

# # JFC #2 Real Time Monitor

# In[4]:

import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as colors
import matplotlib as mpl
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import xarray
import os.path as path
import datetime as dt
import warnings
import cosmicsense as cs
import glob
import os
import copy
import wradlib
from scipy.optimize import minimize_scalar, minimize
import scipy.stats as stats
from scipy import spatial
from matplotlib.colors import rgb2hex
from IPython.display import Image
from pandas.plotting import register_matplotlib_converters
from matplotlib import ticker
register_matplotlib_converters()


warnings.simplefilter('once', RuntimeWarning)

#ids = [10,11]
#ids = eval(sys.argv[1])
#ids_all = np.arange(1,16).astype("int")
ids = [1,4,21,22,26,27]
ids_all = np.array([1,2,4,9,11,12,13,21,22,26,27])


#ids_all = np.arange(1,16).astype("int")


#fpath = "/home/maik/b2drop/cosmicsense/inbox/wuestebach/timeseries/crns/merged/"
fpath = "/media/x/cosmicsense/data/marquardt/crns_merged/remote/"
crns = {}
for id in ids:
    df = pd.read_csv(path.join(fpath, "%d_CRNS.txt" % id), sep="\t", na_values=-99.)
    # discard first records as they are mostly rubbish
    df = df[~(df.rec_id==1)]
    df = df[1:]
    df.datetime = [pd.to_datetime(dtime.strftime("%Y-%m-%d %H:%M:%S")) for dtime in pd.to_datetime(df.datetime, utc=None)]
    df = df.set_index("datetime")
    if id in [4]:
        # two CRS-1000-B
        df["cph"] = (df.counts1 + df.counts2) / cs.conv.s_to_h(df.nsecs1)
#    elif id in [9,15]:
#        # bare counter on counts1, Lab-C on counts2
#        df["cph"] = df.counts2 / cs.conv.s_to_h(df.nsecs2)
    else:
        df["cph"] = df.counts1 / cs.conv.s_to_h(df.nsecs1)
    print("%d: %s to %s" % (id, df.index[0], df.index[-1]) )
    crns[id] = df


formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((-1,1))


plt.rc('font', **{'size'   : 12})

colors = plt.cm.tab20(np.linspace(0,1,len(ids)))

fig, ax = plt.subplots(nrows=4, ncols=3, figsize=(10,7), sharex=True)
ax = ax.ravel()

tend = dt.datetime.now()
tstart = tend - dt.timedelta(days=10)

voltcol = "tab:green"

legend_elements = [plt.Line2D([0], [0], lw=0, marker="o", mfc="None", mec="black", ms=4, label="cph"),
                   plt.Line2D([0], [0], lw=0, marker="o", mfc="None", mec=voltcol,  ms=4, label="voltage (V)")]

for i, id in enumerate(ids_all):
    plt.sca(ax[i])
    if id in ids:
        plt.plot(crns[id][tstart:tend].index, crns[id].loc[tstart:tend, "cph"],
                 "ko", ms=2, mfc="None", mec="black", alpha=0.2)
        tmp = crns[id].rolling("12H").mean()
        plt.plot(tmp[tstart:tend].index-dt.timedelta(seconds=6*3600), tmp.loc[tstart:tend, "cph"],
                 "k-")
        #ax[i].yaxis.set_major_formatter(formatter)
        plt.grid()
        if np.nanmin(crns[id].cph)==0:
            plt.ylim(bottom=0)
        ax2 = plt.twinx(ax[i])
        plt.plot(crns[id][tstart:tend].index, crns[id].loc[tstart:tend, "volt"],
                 "ko", ms=2, mfc="None", mec=voltcol)
        ax2.spines['right'].set_color(voltcol)
        ax2.tick_params(axis='y', colors=voltcol)
        plt.ylim(11,14)
        plt.axvline(tend, ymin=0, ymax=10000, color="tab:red", ls="dashed")
    else:
        plt.grid()
        plt.text(tstart, 0.5, "Probe not online, yet", verticalalignment="center")
        ax[i].get_yaxis().set_ticks([])
        ax2 = plt.twinx(ax[i])
        ax2.spines['right'].set_color(voltcol)
        ax2.tick_params(axis='y', colors=voltcol)
        plt.ylim(11,14)
    if (i+1) % 3 > 0:
        ax2.get_yaxis().set_ticks([])
    if i==0:
        _ = plt.legend(handles=legend_elements, fontsize=8, loc="lower left", ncol=2)
    ax[i].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    #plt.sca(ax[i])
    ylim = plt.ylim()
    plt.text(tstart, ylim[1]-0.08*(ylim[1]-ylim[0]), "#"+str(id), color="tab:red",
             verticalalignment="top", weight=500, fontsize=14,
             bbox=dict(facecolor='white', edgecolor="None", alpha=0.7, pad=0.))
#plt.sca(ax[15])

plt.suptitle("Last update: %s" % tend.strftime("%a, %d %b, %H:%M"), y=1.01)
#plt.axis('off')
fig.autofmt_xdate()
plt.tight_layout(pad=1.01, w_pad=-0.05, h_pad=0.1)

plt.savefig("/media/x/cosmicsense/git/misc/marquardt/crnsmonitor.png", dpi=300, bbox_inches="tight")
