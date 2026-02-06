.. _howto:

=============
How-to guides
=============

Practical recipes for common tasks. Each guide assumes you have already
installed condastats (see :doc:`installation`).

.. contents:: Recipes
   :local:
   :depth: 1


Filter by time period
=====================

**Single month**

Pass ``--month`` (CLI) or the ``month`` keyword (Python):

.. tab-set::

   .. tab-item:: CLI

      .. code-block:: console

         $ condastats overall pandas --month 2024-01

   .. tab-item:: Python

      .. code-block:: python

         overall("pandas", month="2024-01")

**Date range**

Pass ``--start_month`` and ``--end_month`` together:

.. tab-set::

   .. tab-item:: CLI

      .. code-block:: console

         $ condastats overall pandas --start_month 2024-01 --end_month 2024-06

   .. tab-item:: Python

      .. code-block:: python

         overall("pandas", start_month="2024-01", end_month="2024-06")

**Monthly breakdown**

Add ``--monthly`` to split the result by month instead of summing:

.. tab-set::

   .. tab-item:: CLI

      .. code-block:: console

         $ condastats overall pandas --start_month 2024-01 --end_month 2024-03 --monthly

   .. tab-item:: Python

      .. code-block:: python

         overall("pandas", start_month="2024-01", end_month="2024-03", monthly=True)


Group downloads by dimension
============================

condastats has four grouping subcommands. Each one splits download counts
by a different column in the dataset:

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - Subcommand / function
     - Groups by
     - Example values
   * - ``pkg_platform``
     - Platform architecture
     - ``linux-64``, ``osx-arm64``, ``win-64``
   * - ``data_source``
     - Channel or repository
     - ``anaconda``, ``conda-forge``
   * - ``pkg_version``
     - Package version
     - ``1.5.3``, ``2.0.0``
   * - ``pkg_python``
     - Python version used
     - ``3.10``, ``3.11``, ``3.12``

All four accept the same time-filtering options (``--month``,
``--start_month``/``--end_month``, ``--monthly``).

.. tab-set::

   .. tab-item:: CLI

      .. code-block:: console

         $ condastats data_source pandas --month 2024-01

   .. tab-item:: Python

      .. code-block:: python

         from condastats import data_source
         data_source("pandas", month="2024-01")


Filter overall downloads by multiple criteria
==============================================

The ``overall`` subcommand (and :func:`~condastats.overall` function) supports
additional filter flags to narrow results by platform, data source, package
version, and Python version -- all at once:

.. tab-set::

   .. tab-item:: CLI

      .. code-block:: console

         $ condastats overall pandas --month 2024-01 \
             --pkg_platform linux-64 \
             --data_source conda-forge \
             --pkg_python 3.11

   .. tab-item:: Python

      .. code-block:: python

         overall(
             "pandas",
             month="2024-01",
             pkg_platform="linux-64",
             data_source="conda-forge",
             pkg_python="3.11",
         )


Compare multiple packages
=========================

Pass multiple package names on the command line, or a list in Python:

.. tab-set::

   .. tab-item:: CLI

      .. code-block:: console

         $ condastats overall pandas numpy scipy --month 2024-01

   .. tab-item:: Python

      .. code-block:: python

         overall(["pandas", "numpy", "scipy"], month="2024-01")

This works with every subcommand, not just ``overall``.


Get the raw DataFrame
=====================

By default :func:`~condastats.overall` aggregates results into a
:class:`pandas.Series`. Pass ``complete=True`` to get the full, unaggregated
:class:`pandas.DataFrame`:

.. code-block:: python

   df = overall("pandas", month="2024-01", complete=True)
   df.head()

.. tip::

   This is useful when you want to do custom grouping or further analysis
   with the full dataset.


Use condastats in Jupyter notebooks
====================================

condastats works out of the box in Jupyter. Because every function returns a
pandas object, results render as rich HTML tables:

.. code-block:: python

   from condastats import overall, pkg_platform

   # A Series renders as a nice table in Jupyter
   overall(["pandas", "numpy"], month="2024-01")

You can also call the CLI from a notebook cell with a ``!`` prefix:

.. code-block:: text

   !condastats pkg_platform pandas --month 2024-01


Run condastats without installing
=================================

.. seealso::

   :ref:`installation` for full details on all installation methods.

If you just want a quick one-off query:

.. tab-set::

   .. tab-item:: uvx

      .. code-block:: console

         $ uvx condastats overall pandas --month 2024-01

   .. tab-item:: pipx run

      .. code-block:: console

         $ pipx run condastats overall pandas --month 2024-01

These download condastats into a temporary environment, run the command, and
clean up afterwards -- no permanent installation required.
