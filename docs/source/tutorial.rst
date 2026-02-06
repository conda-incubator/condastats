.. _tutorial:

========
Tutorial
========

This tutorial walks you through your first conda download statistics query.
By the end, you will know how to use both the command-line tool and the
Python API.

.. contents:: In this tutorial
   :local:
   :depth: 1


Prerequisites
=============

Install condastats before you begin (see :doc:`installation`). Verify it
works:

.. code-block:: console

   $ condastats --version

You should see the installed version number.


Step 1: Get total downloads for a package
=========================================

The simplest query returns the *total* download count for a package since
2017:

.. code-block:: console

   $ condastats overall pandas

.. code-block:: text

   pkg_name
   pandas    24086379
   Name: counts, dtype: int64

This sums all downloads across every month, platform, and channel in the
`Anaconda public dataset <https://github.com/ContinuumIO/anaconda-package-data>`_.


Step 2: Focus on a specific month
==================================

Add ``--month`` to restrict the query to a single month:

.. code-block:: console

   $ condastats overall pandas --month 2024-01

.. code-block:: text

   pkg_name
   pandas    932443
   Name: counts, dtype: int64


Step 3: See the monthly trend
=============================

Provide a range with ``--start_month`` and ``--end_month``, then pass
``--monthly`` to get the per-month breakdown:

.. code-block:: console

   $ condastats overall pandas --start_month 2024-01 --end_month 2024-03 --monthly

.. code-block:: text

   pkg_name  time
   pandas    2024-01     932443.0
             2024-02    1049595.0
             2024-03    1268802.0
   Name: counts, dtype: float64


Step 4: Break down by a dimension
==================================

Use a different subcommand to group downloads by platform, data source,
package version, or Python version. For example, to see which platforms
download pandas the most:

.. code-block:: console

   $ condastats pkg_platform pandas --month 2024-01

.. code-block:: text

   pkg_name  pkg_platform
   pandas    linux-32              22.0
             linux-64          461318.0
             linux-aarch64      19375.0
             osx-64            131849.0
             osx-arm64          68324.0
             win-32               155.0
             win-64            251400.0
   Name: counts, dtype: float64


Step 5: Use the Python API
==========================

Everything you can do on the command line is also available as a Python
function. Open a Python shell or Jupyter notebook:

.. code-block:: python

   >>> from condastats import overall, pkg_platform

   >>> overall("pandas", month="2024-01")
   pkg_name
   pandas    932443
   Name: counts, dtype: int64

   >>> pkg_platform("pandas", month="2024-01")
   pkg_name  pkg_platform
   pandas    linux-32              22.0
             linux-64          461318.0
             ...
   Name: counts, dtype: float64

Every function returns a :class:`pandas.Series` (or :class:`pandas.DataFrame`
when using ``complete=True`` in :func:`~condastats.overall`), so you can
immediately chain pandas operations on the result.


Step 6: Compare multiple packages
==================================

Both the CLI and the Python API accept multiple package names:

.. code-block:: console

   $ condastats overall pandas numpy dask --month 2024-01

.. code-block:: python

   >>> overall(["pandas", "numpy", "dask"], month="2024-01")
   pkg_name
   dask      221200
   numpy    3345821
   pandas    932443
   Name: counts, dtype: int64


What next?
==========

* Browse the :doc:`howto` for specific recipes.
* Check the :doc:`reference/api` and :doc:`reference/cli` for every option.
* Read :doc:`explanation` to understand the data source and how condastats
  works under the hood.
