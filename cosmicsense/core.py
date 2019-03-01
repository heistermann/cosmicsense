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

    corrfact_baro
    corrfact_vapor_rosolem
    n_to_theta_desilets

"""

import numpy as np
import pandas as pd
import cosmicsense.conv as conv


def corrfact_vapor_rosolem(h, h_ref=None, const=0.0054):
    """Correction factor for vapor correction from absolute humidity (g/m3).

    The equation was suggested by Rosolem et al. (2013).

    If no reference value for absolute humidity ``h_ref`` is provided,
    the average value will be used.

    Parameters
    ----------
    h : float or array of floats
       Absolute humidity (g / m3)
    h_ref : float
       Reference value for absolute humidity
    const : float
       Empirical constant, defaults to 0.0054

    Returns
    -------
    output : float or array of floats
       Correction factor for water vapor effect (dimensionless)

    """
    if h_ref is None:
        h_ref = np.mean(h)
    return 1 + const * (h - h_ref)


def corrfact_baro(p, p_0, L):
    """Compute correction factor for barometric effects.

    The equation was suggested by Zreda et al. (2012). For default values of
    the mass attenuation length for high-energy neutrons ``L``, refer to Fig. 1
    in Andreasen et al. (2017).

    Parameters
    ----------
    p : float or array of floats
       Barometric pressure at the probe (mbar)
    p_0 : float
       Reference value for barometric pressure (mbar)
    L : float
       Mass attenuation length for high-energy neutrons

    Returns
    -------
    output : float or array of floats
       Correction factor for barometric effects (dimensionless)

    """
    return np.exp( conv.pa_to_gscm( conv.mbar_to_pa(p_0 - p) ) / L )


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
