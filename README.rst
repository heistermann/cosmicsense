``cosmicsense``: From Cosmic Ray Neutron Counts to Soil Moisture Products
=========================================================================

.. image:: https://travis-ci.com/heistermann/cosmicsense.svg?branch=master
    :target: https://travis-ci.com/heistermann/cosmicsense

.. image:: https://readthedocs.org/projects/cosmicsense/badge/?version=latest
    :target: https://cosmicsense.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

This package provides a platform to collect algorithms and workflows to estimate
soil moisture from cosmic ray neutron counters, and compare such estimates with
other soil moisture products.


Install
-------

``cosmicsense`` comes as a pure Python package. It requires several dependencies
as listed in ``requirements.txt``. We recommend ``conda`` for dependency management.

1. Install Miniconda (https://conda.io/miniconda.html).

2. Add the ``conda-forge`` channel as the new default::

      $ conda config --add channels conda-forge

3. Create a new ``conda`` environment::

      $ conda create --name cosmicsense python=3.7

4. Activate the new environment:

    **Linux**::

       $ source activate cosmicsense

    **Windows**::

       > activate cosmicsense

5. Install dependencies::

      (cosmicsense) $ conda install numpy scipy matplotlib pandas jupyter

6. Install ``cosmicsense`` package from source::

      (cosmicsense) $ python setup.py install
