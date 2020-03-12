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
    horizontal_weight_zreda2008a
    horizontal_weight_zreda2008b
    rescale_r
    horizontal_weight_koehli
    horizontal_weight_koehli_approx
    penetration_depth_franz
    vertical_weight_franz
    D86
    vertical_weight_koehli

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


def theta_to_n_desilets(theta, n0, a0=0.0808, a1=0.372, a2=0.115, rhob=1500., rhow=1000.):
    """Convert theta to neutron counts.

    Based on Desilets et al. (2010).

    Parameters
    ----------
    theta : float
        Volumetric soil water content (m3/m3)
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
        Number of neutron counts.

    """
    return n0 * (a1 + a0/(theta*(rhow/rhob) + a2))


def horizontal_weight_zreda2008a(r):
    """Horizontal weights according to Zreda et al. (2008).

    The actual function was presented in Schroen et al. (2017).

    Parameters
    ----------
    r : float or 1d array of floats
       Distance to the CRNS probe (in meters)

    """
    return np.exp(-r / 127.)


def horizontal_weight_zreda2008b(r, a1=1.311e-2, a2=9.423e-5, a3=3.2e-7, a4=3.95e-10):
    """Presented by Bogena et al. (2013, Eq. 13), fitted to Zreda et al. (2008).

    Bogena et al. (2013) fitted a polynomial function through the relationship between
    cumulative fraction of counts (CFoC) and CRP footprint radius (r) presented by
    Zreda et al. (2008).

    Parameters
    ----------
    r : float or 1d array of floats
       Distance to the CRNS probe (in meters)
    a1, a2, a3, a4 : float
       Empirical parameters

    """
    return 1 - a1 * r + a2 * r**2 - a3 * r**3 + a4 * r**4


def F0(p0=3.7):
    return p0


def F1(theta, h, p0=8735., p1=22.689, p2=11720., p3=0.00978, p4=9306., p5=0.003632):
    return p0 * (1 + p3 * h) * np.exp(-p1 * theta) + p2 * (1 + p5 * h) - p4 * theta


def F2(theta, h, p0=0.027925, p1=6.6577, p2=0.028544, p3=0.002455, p4=6.851e-5, p5=12.2755):
    return ((p4 * h - p0) * np.exp(-p1 * theta / (1 + p5 * theta)) + p2) * (1 + p3 * h)


def F3(theta, h, p0=247970., p1=23.289, p2=374655., p3=0.00191, p4=258552.):
    return p0 * (1 + p3 * h) * np.exp(-p1 * theta) + p2 - p4 * theta


def F4(theta, h, p0=0.054818, p1=21.032, p2=0.6373, p3=0.0791, p4=5.425e-4):
    return p0 * np.exp(-p1 * theta) + p2 - p3 * theta +  p4 * h


def F5(theta, h, p0=39006., p1=15002330, p2=2009.24, p3=0.01181, p4=3.146, p5=16.7417, p6=3727.):
    return (p0 - p1 / (p2 * theta + h - 0.13)) * (p3 - theta) * np.exp(-p4 * theta) - p5 * h * theta + p6

def F6(theta, h, p0=6.031e-5, p1=98.5, p2=0.0013826):
    return p0 * (h + p1) + p2 * theta


def F7(theta, h, p0=11747., p1=55.033, p2=4521., p3=0.01998, p4=0.00604, p5=3347.4, p6=0.00475):
    return (p0 * (1 - p6 * h) * np.exp(-p1 * theta * (1 - p4 * h)) + p2 - p5 * theta) * (2 + p3 * h)


def F8(theta, h, p0=0.01543, p1=13.29, p2=0.01807, p3=0.0011, p4=8.81e-5, p5=0.0405, p6=26.74):
    return ((p4 * h - p0) * np.exp(-p1 * theta / (1 + p5 * h + p6 * theta)) + p2) * (2 + p3 * h)


def Fp(press, p0=0.4922, p1=0.86):
    return p0 / (p1 - np.exp(-press / 1013.))


def Fveg(theta, Hveg, p0=0.17, p1=0.41, p2=9.25):
    return 1 - p0 * (1 - np.exp(-p1 * Hveg)) * (1 + np.exp(-p2 * theta))


def rescale_r(r, press, Hveg, theta):
    return r / Fp(press) / Fveg(theta, Hveg)


def horizontal_weight_koehli(r, press, Hveg, theta, h):
    """Horizontal weights presented by Koehli et al. (2015), modified by Schroen et al. (2017)

    Parameters
    ----------
    r : float or 1d array of floats
       Distance to the CRNS probe (in meters)

    """
    # Container
    r = np.asarray(r)
    x = np.zeros(r.shape) * np.nan
    r_st = rescale_r(r, press, Hveg, theta)
    # Index arrays
    ix1 = r <= 1
    ix2 = (r > 1) & (r <= 50)
    ix3 = (r > 50) & (r < 600)
    # r <= 1 m
    r1 = r[ix1]
    x[ix1] = (F1(theta, h) * np.exp(-F2(theta, h) * r_st[ix1]) + F3(theta, h) * np.exp(-F4(theta, h) * r_st[ix1])) \
    * (1 - np.exp(-F0() * r_st[ix1]))
    # r > 1m and r <= 50 m
    r2 = r[ix2]
    x[ix2] = F1(theta, h) * np.exp(-F2(theta, h) * r_st[ix2]) + F3(theta, h) * np.exp(-F4(theta, h) * r_st[ix2])
    # r > 50 m and r < 600 m
    r3 = r[ix3]
    x[ix3] = F5(theta, h) * np.exp(-F6(theta, h) * r_st[ix3]) + F7(theta, h) * np.exp(-F8(theta, h) * r_st[ix3])

    return x


def horizontal_weight_koehli_approx(r):
    """Approximation adopted from Appendix B of Schroen et al. (2017).

    Parameters
    ----------
    r : float or 1d array of floats
       Distance to the CRNS probe (in meters)

    """
    r = np.asarray(r)
    x = np.zeros(r.shape) * np.nan
    # Index arrays
    ix1 = r <= 1
    ix2 = r > 1
    r1 = r[ix1]
    x[ix1] = (30 * np.exp(-r1 / 1.6) + np.exp(-r1 / 100)) * (1 - np.exp(-3.7 * r1))
    r2 = r[ix2]
    x[ix2] = 30 * np.exp(-r2 / 1.6) + np.exp(-r2 / 100)

    return x


def penetration_depth_franz(theta):
    """Vertical penetration depth as a function of theta.

    Based on Franz et al. (2012).

    Parameters
    ----------
    theta : float or array of floats
       Volumetric soil moisture (m3/m3)

    Returns
    -------
    output : float or array of floats
       Vertical penetration depth (cm)

    """
    return 5.8 / (theta + 0.0829)


def vertical_weight_franz(depth, theta):
    """Based on Franz et al. (2012).

    Parameters
    ----------
    depth : float or 1d array of floats
       depth (cm) for which a weight should be returned
    theta : float or array of floats
       Average volumetric soil moisture (m3/m3) in the footprint

    Returns
    -------
    output : float or array of floats of shape ``(len(depth), len(theta))``, squeezed
       Vertical weights

    """
    depth = np.atleast_1d(depth)
    theta = np.atleast_1d(theta)
    D = penetration_depth_franz(theta)
    depth, D = np.meshgrid(depth, D)
    x = np.zeros(depth.shape)
    ix = depth <= D
    x[ix] = 1. - depth[ix] / D[ix]

    return np.squeeze(x)


def D86(r, theta, press, Hveg, rhob, p0=8.321, p1=0.14249, p2=0.96655, p3=0.01, p4=20., p5=0.0429):
    """Penetration depth, or rather the depth within which 86 % of neutrons probed the soil.

    Based on Koehli et al. (2015) and Schroen et al. (2017).

    Parameters
    ----------
    depth : float or 1d array of floats
       depth (cm) for which a weight should be returned
    theta : float or array of floats
       Average volumetric soil moisture (m3/m3) in the footprint
    press : float
       Barometric pressure (hPa)
    Hveg : float
       Vegetation height (UNIT???)
    rhob : float
       Soil bulk density (kg/l)
    p0 - p5: floats
       Parameters

    Returns
    -------
    output : float or array of floats of shape ``(len(r), len(theta))``, squeezed
       Penetration depth (cm)

    """
    r = np.atleast_1d(r)
    theta = np.atleast_1d(theta)
    r, theta = np.meshgrid(r, theta, indexing="ij")
    x = (1 / rhob) * (p0 + p1 * (p2 + np.exp(-p3 * rescale_r(r, press, Hveg, theta))) * (p4 + theta) / (p5 + theta))
    return np.squeeze(x)


def vertical_weight_koehli(r, depth, theta, press, Hveg, rhob):
    """Vertical weights for gven distance, depth, and environmental conditions.

    Based on Koehli et al. (2015) and Schrön et al. (2017).

    Parameters
    ----------
    r : float of 1d-array of floats
    depth : float or 1d-array of floats
    theta : float
    press : float
    Hveg : float
    rhob : float

    Returns
    -------
    output : float or array of floats of shape ``(len(r), len(depth))``, squeezed
       Dimensionless weights

    """
    r = np.atleast_1d(r)
    depth = np.atleast_1d(depth)
    D = D86(r, theta, press, Hveg, rhob)
    depth, D = np.meshgrid(depth, D, indexing="ij")
    x = np.exp(-2 * depth / D)
    return np.squeeze(x)


if __name__ == '__main__':
    print('cosmicsense: Calling module <core> as main...')
