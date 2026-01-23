==========
condastats
==========

.. image:: https://img.shields.io/pypi/v/condastats.svg
        :target: https://pypi.org/project/condastats/
        :alt: PyPI Version

.. image:: https://img.shields.io/conda/vn/conda-forge/condastats.svg
        :target: https://anaconda.org/conda-forge/condastats
        :alt: Conda Version

.. image:: https://img.shields.io/pypi/pyversions/condastats.svg
        :target: https://pypi.org/project/condastats/
        :alt: Python Versions

.. image:: https://github.com/conda-incubator/condastats/actions/workflows/tests.yml/badge.svg
        :target: https://github.com/conda-incubator/condastats/actions/workflows/tests.yml
        :alt: CI Status

.. image:: https://readthedocs.org/projects/condastats/badge/?version=latest
        :target: https://condastats.readthedocs.io/en/latest/
        :alt: Documentation Status

.. image:: https://img.shields.io/pypi/l/condastats.svg
        :target: https://github.com/conda-incubator/condastats/blob/main/LICENSE
        :alt: License

A command-line tool and Python library to query download statistics for conda packages from the Anaconda public dataset.

Features
--------

* Query overall download counts for any conda package
* Filter by time period (specific month or date range)
* Group statistics by platform, Python version, package version, or data source
* Support for multiple packages in a single query
* Works with historical data from 2017 onwards

Installation
------------

Using conda (recommended)::

    conda install -c conda-forge condastats

Using pip::

    pip install condastats

Usage
-----

Command Line
~~~~~~~~~~~~

Get overall download counts for a package::

    condastats overall pandas --month 2024-01

Get downloads grouped by platform::

    condastats pkg_platform numpy --month 2024-01

Get downloads grouped by data source (anaconda vs conda-forge)::

    condastats data_source scipy --month 2024-01

Query multiple packages::

    condastats overall pandas numpy dask --month 2024-01

Python API
~~~~~~~~~~

.. code-block:: python

    from condastats import overall, pkg_platform, data_source

    # Get total downloads for pandas in January 2024
    downloads = overall("pandas", month="2024-01")
    print(downloads)

    # Get downloads by platform
    by_platform = pkg_platform("pandas", month="2024-01")
    print(by_platform)

    # Get downloads over a date range
    downloads = overall("numpy", start_month="2024-01", end_month="2024-06")
    print(downloads)

Documentation
-------------

Full documentation is available at https://condastats.readthedocs.io

License
-------

* Free software: BSD-3-Clause license

Credits
-------

Created by `Sophia Man Yang <https://github.com/sophiamyang>`_.

Maintained by the `conda-incubator <https://github.com/conda-incubator>`_ community.
