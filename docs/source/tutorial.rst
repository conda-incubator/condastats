.. _tutorial:

========
Tutorial
========

This tutorial walks you through your first conda download statistics query.
By the end, you will know how to use both the command-line tool and the
Python API.

.. note::

   Install condastats before you begin (see :doc:`installation`). Verify it
   works by running ``condastats --version``.


Step 1: Get total downloads for a package
=========================================

The simplest query returns the *total* download count for a package since
2017:

.. tab-set::

   .. tab-item:: CLI

      .. code-block:: console

         $ condastats overall pandas

   .. tab-item:: Python

      .. code-block:: python

         >>> from condastats import overall
         >>> overall("pandas")

.. code-block:: text

   pkg_name
   pandas    24086379
   Name: counts, dtype: int64

This sums all downloads across every month, platform, and channel in the
`Anaconda public dataset <https://github.com/ContinuumIO/anaconda-package-data>`_.


Step 2: Focus on a specific month
==================================

Add ``--month`` to restrict the query to a single month:

.. tab-set::

   .. tab-item:: CLI

      .. code-block:: console

         $ condastats overall pandas --month 2024-01

   .. tab-item:: Python

      .. code-block:: python

         >>> overall("pandas", month="2024-01")

.. code-block:: text

   pkg_name
   pandas    932443
   Name: counts, dtype: int64


Step 3: See the monthly trend
=============================

Provide a range with ``--start_month`` and ``--end_month``, then pass
``--monthly`` to get the per-month breakdown:

.. tab-set::

   .. tab-item:: CLI

      .. code-block:: console

         $ condastats overall pandas --start_month 2024-01 --end_month 2024-03 --monthly

   .. tab-item:: Python

      .. code-block:: python

         >>> overall("pandas", start_month="2024-01", end_month="2024-03", monthly=True)

.. code-block:: text

   pkg_name  time
   pandas    2024-01     932443.0
             2024-02    1049595.0
             2024-03    1268802.0
   Name: counts, dtype: float64


Step 4: Break down by a dimension
==================================

Use a different subcommand to group downloads by platform, data source,
package version, or Python version:

.. tab-set::

   .. tab-item:: CLI

      .. code-block:: console

         $ condastats pkg_platform pandas --month 2024-01

   .. tab-item:: Python

      .. code-block:: python

         >>> from condastats import pkg_platform
         >>> pkg_platform("pandas", month="2024-01")

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


Step 5: Compare multiple packages
==================================

Both the CLI and the Python API accept multiple package names:

.. tab-set::

   .. tab-item:: CLI

      .. code-block:: console

         $ condastats overall pandas numpy dask --month 2024-01

   .. tab-item:: Python

      .. code-block:: python

         >>> overall(["pandas", "numpy", "dask"], month="2024-01")

.. code-block:: text

   pkg_name
   dask      221200
   numpy    3345821
   pandas    932443
   Name: counts, dtype: int64

.. tip::

   Every function returns a :class:`pandas.Series` (or
   :class:`pandas.DataFrame` with ``complete=True``), so you can
   immediately chain pandas operations on the result.


What next?
==========

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: :octicon:`tasklist` How-to guides
      :link: howto
      :link-type: doc

      Practical recipes for filtering, grouping, Jupyter, and more.

   .. grid-item-card:: :octicon:`code` API reference
      :link: reference/api
      :link-type: doc

      Full documentation for every function and parameter.

   .. grid-item-card:: :octicon:`terminal` CLI reference
      :link: reference/cli
      :link-type: doc

      All subcommands, options, and exit codes.

   .. grid-item-card:: :octicon:`light-bulb` Explanation
      :link: explanation
      :link-type: doc

      How the data source and query pipeline work.
