.. _api-reference:

==================
Python API
==================

All public functions are available directly from the top-level
``condastats`` package:

.. code-block:: python

   from condastats import overall, pkg_platform, data_source, pkg_version, pkg_python

Every function returns a :class:`pandas.Series` (download counts indexed by
package name and, optionally, by grouping dimension and/or time). The
:func:`overall` function can also return a :class:`pandas.DataFrame` when
``complete=True``.


S3-backed functions
-------------------

These convenience functions read data from the public Anaconda S3 bucket
via **dask** and return aggregated pandas results. They require ``dask``
and ``s3fs`` to be installed.

.. autofunction:: condastats.overall

.. autofunction:: condastats.pkg_platform

.. autofunction:: condastats.data_source

.. autofunction:: condastats.pkg_version

.. autofunction:: condastats.pkg_python


Pure-pandas query functions
---------------------------

These functions operate on any :class:`pandas.DataFrame` that follows the
Anaconda package-data schema (columns: ``pkg_name``, ``counts``, ``time``,
``pkg_platform``, ``data_source``, ``pkg_version``, ``pkg_python``).

They have **no dependency on dask or s3fs** and work anywhere pandas runs,
including Pyodide.

.. autofunction:: condastats.query_overall

.. autofunction:: condastats.query_grouped

.. autofunction:: condastats.top_packages


Common parameters
-----------------

The S3-backed functions share a core set of parameters:

``package``
   One or more package names. Pass a string for a single package or a list
   of strings for multiple packages.

``month``
   A specific month in ``YYYY-MM`` format (e.g., ``"2024-01"``).
   Mutually exclusive with ``start_month``/``end_month``.

``start_month`` / ``end_month``
   Define a date range. Both must be provided together, in ``YYYY-MM``
   format.

``monthly``
   When ``True``, return a per-month breakdown instead of a single total.
   Adds a ``time`` level to the result index.


Return types
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Scenario
     - Return type
   * - Default (aggregated)
     - :class:`pandas.Series` with a :class:`pandas.Index` or
       :class:`pandas.MultiIndex`
   * - ``overall(..., complete=True)``
     - :class:`pandas.DataFrame` with all original columns
