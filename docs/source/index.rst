condastats
==========

**condastats** is a command-line tool and Python library to query download
statistics for conda packages from the `Anaconda public dataset`_.

.. code-block:: console

   $ condastats overall pandas --month 2024-01
   pkg_name
   pandas    932443
   Name: counts, dtype: int64

.. code-block:: python

   from condastats import overall

   overall("pandas", month="2024-01")

.. _Anaconda public dataset: https://github.com/ContinuumIO/anaconda-package-data

Getting started
---------------

.. toctree::
   :maxdepth: 1

   installation
   tutorial

How-to guides
-------------

Practical step-by-step guides for common tasks.

.. toctree::
   :maxdepth: 1

   howto

Reference
---------

Technical descriptions of the Python API and CLI.

.. toctree::
   :maxdepth: 1

   reference/api
   reference/cli

Background
----------

Explanation and context that help you understand condastats and its data.

.. toctree::
   :maxdepth: 1

   explanation


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
