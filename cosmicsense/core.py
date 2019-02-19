#!/usr/bin/env python
# Copyright (c) 2018-2019, cosmicsense developers.
# Distributed under the MIT License. See LICENSE.txt for more info.

"""
Fundamental equations
^^^^^^^^^^^^^^^^^^^^^

Model `core` contains the fundamental equations of converting neutron counts
to soil moisture.

.. currentmodule:: cosmicsense.core

.. autosummary::
   :nosignatures:
   :toctree: generated/




"""
import numpy as np


def n_to_theta(n, a=200., b=1.6):
    """Convert neutron counts to theta.

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
        Density of water (/)kg/m3)

    Returns
    -------
    output : float
        Volumetric soil water content (m3/m3)

    """
    return (a0 / (n/n0 -a1) - a2) * rhob / rhow


if __name__ == '__main__':
    print('cosmicsense: Calling module <core> as main...')
