#!/usr/bin/env python
# Copyright (c) 2018-2019, cosmicsense developers.
# Distributed under the MIT License. See LICENSE.txt for more info.

"""
Fundamental equations
^^^^^^^^^^^^^^^^^^^^^

Module ``core`` contains the fundamental equations of converting neutron counts
to soil moisture.

.. currentmodule:: cosmicsense.core

.. autosummary::
   :nosignatures:
   :toctree: generated/

    n_to_theta_desilets

"""

import numpy as np
import pandas as pd

def n_to_theta_desilets(n, n0, a0=0.0808, a1=0.372, a2=0.115, rhob=1500., rhow=1000.):
    """Convert neutron counts to theta.

    Based on Desilets et al. (2010).

    Parameters
    ----------
    n : integer
        Number of neutron counts.
    n0 : integer
        Local calibration factor
    a0 : float
        Parameter
    a1 : float
        Parameter
    a2 : float
        Parameter
    rhob : float
        Soil bulk density (kg/m3)
    rhow : float
        Density of water (kg/m3)

    Returns
    -------
    output : float
        Volumetric soil water content (m3/m3)

    """
    return ((a0 / (n/n0 -a1)) - a2) * rhob / rhow


if __name__ == '__main__':
    print('cosmicsense: Calling module <core> as main...')
