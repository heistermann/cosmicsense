#!/usr/bin/env python
# Copyright (c) 2018-2019, cosmicsense developers.
# Distributed under the MIT License. See LICENSE.txt for more info.

"""
Converting between units
^^^^^^^^^^^^^^^^^^^^^^^^

Module ``conv`` contains phyicsal constants as well as conversion functions
between physical units which are intended to increase comprehensibility and
clarity of code.

.. currentmodule:: cosmicsense.conv

.. autosummary::
   :nosignatures:
   :toctree: generated/

    pa_to_gscm
    gscm_to_pa
    mbar_to_pa
    pa_to_mbar
    s_to_h
    h_to_s
    kg_to_g
    g_to_kg
    degc_to_kelvin
    kelvin_to_degc
    temp_to_saturated_vapor_pressure
    absolute_humidity

"""

import numpy as np


# Physical constants or standard values

# Standard barometric pressure at sea level (mbar)
strd_baro_pressure = 1013.25

# Specific gas constant for water vapor (in J/kg/K)
R_s = 461.4



def pa_to_gscm(x):
    """Pascal to g/cm2.

    Parameters
    ----------
    x : float or array of floats
        Air pressure (in Pa)

    Returns
    -------
    output : float or array of floats
        Air pressure (in g/cm2)

    """
    return x / 98.0665


def gscm_to_pa(x):
    """g/cm2 to Pa.

    Parameters
    ----------
    x : float or array of floats
        Air pressure (in g/cm2)

    Returns
    -------
    output : float or array of floats
        Air pressure (in Pa)

    """
    return x * 98.0665


def mbar_to_pa(x):
    """mbar to Pa.

    Parameters
    ----------
    x : float or array of floats
        Air pressure (in mbar)

    Returns
    -------
    output : float or array of floats
        Air pressure (in Pa)

    """
    return x * 100.


def pa_to_mbar(x):
    """Pa to mbar.

    Parameters
    ----------
    x : float or array of floats
        Air pressure (in Pa)

    Returns
    -------
    output : float or array of floats
        Air pressure (in mbar)

    """
    return x / 100.


def s_to_h(x):
    """Seconds to hours

    Parameters
    ----------
    x : float or array of floats
        seconds

    Returns
    -------
    output : float or array of floats
        hours

    """
    return x / 3600.


def h_to_s(x):
    """Hours to seconds

    Parameters
    ----------
    x : float or array of floats
        hours

    Returns
    -------
    output : float or array of floats
        seconds

    """
    return x * 3600.


def kg_to_g(x):
    """kg to g.

    Parameters
    ----------
    x : float or array of floats
        kg

    Returns
    -------
    output : float or array of floats
        g

    """
    return x * 1000.


def g_to_kg(x):
    """g to kg.

    Parameters
    ----------
    x : float or array of floats
        g

    Returns
    -------
    output : float or array of floats
        kg

    """
    return x / 1000.


def degc_to_kelvin(x):
    """Degree Celsius to Kelvin

    Parameters
    ----------
    x : float or array of floats
       Air temperature in deg C

    Returns
    -------
    output : float or array of floats
       Air temperature in Kelvin

    """
    return x + 273.15


def kelvin_to_degc(x):
    """Kelvin to degree Celsius

    Parameters
    ----------
    x : float or array of floats
       Air temperature in Kelvin

    Returns
    -------
    output : float or array of floats
       Air temperature in deg C

    """
    return x - 273.15


def temp_to_saturated_vapor_pressure(temp):
    """August-Roche-Magnus approximation.

    See this `Wikipedia article <https://en.wikipedia.org/wiki/Clausius%E2%80%93Clapeyron_relation#Meteorology_and_climatology>`_
    for further information.

    Parameters
    ----------
    temp : float or array of floats
       Air temperature in deg C

    Returns
    -------
    output : float or array of floats
       Saturated vapor pressure (in mbar)
    """
    return 6.1094 * np.exp(17.625 * temp / (temp + 243.04))


def absolute_humidity(temp, rh):
    """Absolute humidity (g/m3) from air temperature and relative humidity.

    Based on August-Roche-Magnus approximation and ideal law of gases.

    Parameters
    ----------
    temp : float or array of floats
       Air temperature in deg C
    rh : float or array of floats
       Relative humidity (percent)

    Returns
    -------
    output : float or array of floats
       Absolute humidity (g / m3)

    """
    e_s = temp_to_saturated_vapor_pressure(temp)
    e = e_s * rh / 100.
    rho = mbar_to_pa(e) / (R_s * degc_to_kelvin(temp))
    return kg_to_g(rho)

if __name__ == '__main__':
    print('cosmicsense: Calling module <conv> as main...')
