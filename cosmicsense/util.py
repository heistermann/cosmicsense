#!/usr/bin/env python
# Copyright (c) 2018-2019, cosmicsense developers.
# Distributed under the MIT License. See LICENSE.txt for more info.

"""
Helper and utility functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Module ``util`` contains a mixed bag of utilities.

.. currentmodule:: cosmicsense.util

.. autosummary::
   :nosignatures:
   :toctree: generated/

    xy_from_pointshp

"""

import numpy as np
import wradlib


def xy_from_pointshp(shpfile):
    """Get array of xy coords from point shapefile
    """
    shpdata, shplayer = wradlib.io.open_vector(shpfile)
    nfeat = shplayer.GetFeatureCount()
    xy = np.zeros((nfeat,2)) * np.nan
    for i in range(nfeat):
        feat = shplayer.GetFeature(i)
        geom = feat.geometry()
        xy[i,:] = geom.GetPoint()[0:2]
    return(xy)

def distance(pt, pts):
    """Distances of one point `pt` to a set of points `pts`. 
    """
    return np.sqrt((pts[:,0] - pt[0])**2 + (pts[:,1] - pt[1])**2)

if __name__ == '__main__':
    print('cosmicsense: Calling module <util> as main...')
