cosmicsense
============

.. image:: https://travis-ci.org/mapbox/cosmicsense.svg
   :target: https://travis-ci.org/mapbox/cosmicsense

.. image:: https://coveralls.io/repos/mapbox/cosmicsense/badge.png
   :target: https://coveralls.io/r/mapbox/cosmicsense

A package around Cosmic Ray Neutron Sensing


Install
-------

`cosmicsense` comes as a pure Python package. It requires several dependencies
as listed in `requirements.txt`. We recommend `conda` for dependency management.

1. Install Miniconda (https://conda.io/miniconda.html).

2. Add the conda-forge channnel as the new default:

```
$ conda config --add channels conda-forge
```

3. Create a new `conda` environment:

```
$ conda create --name cosmicsense python=3.7
```

4. Activate the new environment:

    Linux:

    ```
    $ source activate wradlib
    ```

    Windows:

    ```
    > activate wradlib
    ```

5. Install dependencies

```
(cosmicsense) $ conda install numpy scipy matplotlib pandas notebook
```

6, Install `cosmicsense` package:

```
(cosmicsense) $ python setup.py install
```
