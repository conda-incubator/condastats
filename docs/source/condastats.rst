============
condastats
============

`condastats <https://github.com/conda-incubator/condastats>`__ is a conda
statistics API with Python interface and Command Line interface. This
project is inspired by
`pypistats <https://pypi.org/project/pypistats/>`__, which is a
python client and CLI API for retrieving PyPI package statistics.


Data source
-----------

Since May 2019, we published hourly summarized download data for all
conda packages, conda-forge channel, and few other channels. The dataset
starts January 2017 and is uploaded once a month. ``condastats`` is built
on top of this `public Anaconda package
data <https://github.com/ContinuumIO/anaconda-package-data>`__ and
return monthly package download statistics.


Command line interface
----------------------

There are five sub-commands in the condastats command: overall,
pkg_platform, data_source, pkg_version, and pkg_python. Run
``condastats --help`` in terminal or run ``!condastats --help`` in
Jupyter Notebook to see all sub-commands:

.. code:: python

    condastats --help


.. parsed-literal::

    usage: condastats [-h]
                      {overall,pkg_platform,data_source,pkg_version,pkg_python}
                      ...

    positional arguments:
      {overall,pkg_platform,data_source,pkg_version,pkg_python}

    optional arguments:
      -h, --help            show this help message and exit


overall
~~~~~~~

``condastats overall`` returns overall download statistics for one or more
packages for specific months and for specified package platform, python
version, package verion, and data source. Run
``condastats overall --help`` in terminal or run
``!condastats overall --help`` in Jupyter Notebook for details:

.. code:: python

    condastats overall --help


.. parsed-literal::

    usage: condastats overall [-h] [--month MONTH] [--start_month START_MONTH]
                              [--end_month END_MONTH] [--monthly]
                              [--pkg_platform PKG_PLATFORM]
                              [--pkg_python PKG_PYTHON]
                              [--pkg_version PKG_VERSION]
                              [--data_source DATA_SOURCE]
                              package [package ...]

    positional arguments:
      package               package name(s)

    optional arguments:
      -h, --help            show this help message and exit
      --month MONTH         month - YYYY-MM (default: None)
      --start_month START_MONTH
                            start month - YYYY-MM (default: None)
      --end_month END_MONTH
                            end month - YYYY-MM (default: None)
      --monthly             return monthly values (default: False)
      --pkg_platform PKG_PLATFORM
                            package platform e.g., win-64, linux-32, osx-64.
                            (default: None)
      --pkg_python PKG_PYTHON
                            Python version e.g., 3.7 (default: None)
      --pkg_version PKG_VERSION
                            Python version e.g., 0.1.0 (default: None)
      --data_source DATA_SOURCE
                            Data source e.g., anaconda, conda-forge (default: None)


The only required argument is ``package``, which can be one or more
packages. When only given package name(s), it will return the total
package download number for all the available `Anaconda public
dataset <https://github.com/ContinuumIO/anaconda-package-data>`__, which
is from 2017 till the end of last month. Here we show total package
download statistics for one package (e.g., pandas) and for multiple packages (e.g., pandas, dask, and numpy)

.. code:: python

    condastats overall pandas


.. parsed-literal::

    pkg_name
    pandas    24086379
    Name: counts, dtype: int64


.. code:: python

    condastats overall pandas dask numpy


.. parsed-literal::

    pkg_name
    dask       7958854
    numpy     53752580
    pandas    24086379
    Name: counts, dtype: int64


We can also get package download statistics for specified month, package
platform, data source, package version, and python version:

.. code:: python

    condastats overall pandas --month 2019-01 --pkg_platform linux-32 --data_source anaconda \
    --pkg_version 0.10.0 --pkg_python 2.6


.. parsed-literal::

    pkg_name
    pandas    12
    Name: counts, dtype: int64


And finally, when we pass in the ``monthly`` argument, we will get
monthly values.

.. code:: python

    condastats overall pandas --start_month 2019-01 --end_month 2019-03 --monthly


.. parsed-literal::

    pkg_name  time
    pandas    2019-01     932443.0
              2019-02    1049595.0
              2019-03    1268802.0
    Name: counts, dtype: float64


pkg_platform, data_source, pkg_version, and pkg_python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The other four subcommands have similiar functions:

-  ``condastats pkg_platform`` returns package download counts by
   package platform.
-  ``condastats data_source`` returns package download counts by data
   source.
-  ``condastats pkg_version`` returns package download counts by package
   version.
-  ``condastats pkg_python`` returns package download counts by python
   version.

The arguments and optional arguments are the same across the four
subcommands. Let’s take a look at ``condastats pkg_platform --help`` and
``condastats data_source --help``:

.. code:: python

    condastats pkg_platform --help


.. parsed-literal::

    usage: condastats pkg_platform [-h] [--month MONTH]
                                   [--start_month START_MONTH]
                                   [--end_month END_MONTH] [--monthly]
                                   package [package ...]

    positional arguments:
      package               package name(s)

    optional arguments:
      -h, --help            show this help message and exit
      --month MONTH         month - YYYY-MM (default: None)
      --start_month START_MONTH
                            start month - YYYY-MM (default: None)
      --end_month END_MONTH
                            end month - YYYY-MM (default: None)
      --monthly             return monthly values (default: False)


.. code:: python

    condastats data_source --help


.. parsed-literal::

    usage: condastats data_source [-h] [--month MONTH] [--start_month START_MONTH]
                                  [--end_month END_MONTH] [--monthly]
                                  package [package ...]

    positional arguments:
      package               package name(s)

    optional arguments:
      -h, --help            show this help message and exit
      --month MONTH         month - YYYY-MM (default: None)
      --start_month START_MONTH
                            start month - YYYY-MM (default: None)
      --end_month END_MONTH
                            end month - YYYY-MM (default: None)
      --monthly             return monthly values (default: False)


Same as ``condastats overall``, we can specify a month, or provide the
start month and the end month of the time period we are interested in.
For example, we can see package download counts for each python version
for pandas for a specific month.

.. code:: python

    condastats pkg_python pandas --month 2019-01


.. parsed-literal::

    pkg_name  pkg_python
    pandas    2.6             1466.0
              2.7           247949.0
              3.3             1119.0
              3.4             9251.0
              3.5           104445.0
              3.6           468838.0
              3.7            99375.0
    Name: counts, dtype: float64


And we can see the monthly counts for each python version with the
``monthly`` flag.

.. code:: python

    condastats pkg_python pandas --start_month 2019-01 --end_month 2019-02 --monthly


.. parsed-literal::

    pkg_name  time     pkg_python
    pandas    2019-01  2.6             1466.0
                       2.7           247949.0
                       3.3             1119.0
                       3.4             9251.0
                       3.5           104445.0
                       3.6           468838.0
                       3.7            99375.0
              2019-02  2.6             1542.0
                       2.7           242518.0
                       3.3             1227.0
                       3.4             8134.0
                       3.5            83393.0
                       3.6           541670.0
                       3.7           171111.0
    Name: counts, dtype: float64


Python interface
----------------

To use the Python interface, we need to import the functions from the
``condastats`` package by running:

.. code:: python

    from condastats.cli import overall, pkg_platform, pkg_version, pkg_python, data_source

Here are the function signatures for these five functions:

.. code:: python

    help(overall)


.. parsed-literal::

    Help on function overall in module condastats.cli:

    overall(package, month=None, start_month=None, end_month=None, monthly=False, pkg_platform=None, data_source=None, pkg_version=None, pkg_python=None)



.. code:: python

    help(pkg_platform)


.. parsed-literal::

    Help on function pkg_platform in module condastats.cli:

    pkg_platform(package, month=None, start_month=None, end_month=None, monthly=False)



.. code:: python

    help(pkg_version)


.. parsed-literal::

    Help on function pkg_version in module condastats.cli:

    pkg_version(package, month=None, start_month=None, end_month=None, monthly=False)



.. code:: python

    help(pkg_python)


.. parsed-literal::

    Help on function pkg_python in module condastats.cli:

    pkg_python(package, month=None, start_month=None, end_month=None, monthly=False)



.. code:: python

    help(data_source)


.. parsed-literal::

    Help on function data_source in module condastats.cli:

    data_source(package, month=None, start_month=None, end_month=None, monthly=False)



Similar to command line interface, we can get the total package download
counts for all the available data since 2017, for a given month, or a
given combination of specifications:

.. code:: python

    overall(['pandas','dask'])




.. parsed-literal::

    pkg_name
    dask       7958854
    pandas    24086379
    Name: counts, dtype: int64



.. code:: python

    overall(['pandas','dask'], month='2019-01')




.. parsed-literal::

    pkg_name
    dask      221200
    pandas    932443
    Name: counts, dtype: int64



.. code:: python

    overall('pandas',month='2019-01', pkg_platform='linux-32',data_source='anaconda',pkg_version='0.10.0',pkg_python=2.6)




.. parsed-literal::

    pkg_name
    pandas    12
    Name: counts, dtype: int64



Similarly, pkg_platform, pkg_version, pkg_python, and data_source
functions will give us package counts for each package platform, package
version, python version, and data source for a given package. Here are
two examples with pkg_python:

.. code:: python

    pkg_python('pandas', month='2019-01')




.. parsed-literal::

    pkg_name  pkg_python
    pandas    2.6             1466.0
              2.7           247949.0
              3.3             1119.0
              3.4             9251.0
              3.5           104445.0
              3.6           468838.0
              3.7            99375.0
    Name: counts, dtype: float64



.. code:: python

    pkg_python('pandas', start_month='2019-01', end_month='2019-02', monthly=True)




.. parsed-literal::

    pkg_name  time     pkg_python
    pandas    2019-01  2.6             1466.0
                       2.7           247949.0
                       3.3             1119.0
                       3.4             9251.0
                       3.5           104445.0
                       3.6           468838.0
                       3.7            99375.0
              2019-02  2.6             1542.0
                       2.7           242518.0
                       3.3             1227.0
                       3.4             8134.0
                       3.5            83393.0
                       3.6           541670.0
                       3.7           171111.0
    Name: counts, dtype: float64



Hope you find ``condastats`` useful! If you have any requests or issues,
please open `an
issue <https://github.com/conda-incubator/condastats/issues>`__ or `a pull
request <https://github.com/conda-incubator/condastats/pulls>`__. If you
have any questions regarding the Anaconda public dataset, please check
out https://github.com/ContinuumIO/anaconda-package-data and open an
issue there.
