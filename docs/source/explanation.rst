.. _explanation:

===========
Explanation
===========

This page provides background on the data that condastats queries and how
the tool works internally.

.. contents::
   :local:
   :depth: 1


The Anaconda public dataset
===========================

condastats is built on top of the `Anaconda public package data
<https://github.com/ContinuumIO/anaconda-package-data>`_, a collection of
hourly-summarized download counts for conda packages published on S3.

Key facts:

* **Coverage:** download records since January 2017.
* **Channels:** includes data from the default ``anaconda`` channel,
  ``conda-forge``, and selected other channels.
* **Update frequency:** the dataset is updated once a month with the
  previous month's data.
* **Format:** Apache Parquet files stored in
  ``s3://anaconda-package-data/conda/monthly/``, organized by year and
  month.


How the data is organized
=========================

Each monthly Parquet file contains one row per download "bucket" with the
following columns:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Column
     - Description
   * - ``pkg_name``
     - Package name (e.g., ``pandas``, ``numpy``).
   * - ``pkg_version``
     - Version string of the downloaded package.
   * - ``pkg_platform``
     - Target platform (e.g., ``linux-64``, ``osx-arm64``, ``win-64``).
   * - ``pkg_python``
     - Python version the package was built for (e.g., ``3.11``).
   * - ``data_source``
     - The channel or repository (e.g., ``anaconda``, ``conda-forge``).
   * - ``counts``
     - Number of downloads in this bucket.
   * - ``time``
     - Month of the download (``YYYY-MM``).


How condastats queries work
===========================

When you run a query, condastats does the following:

1. **Determine the time range.** If you pass ``--month``, a single Parquet
   file is read. If you pass ``--start_month``/``--end_month``, the
   corresponding range of files is read. If neither is given, *all*
   available monthly files are read (this can be slow).

2. **Read from S3.** condastats uses `Dask <https://www.dask.org/>`_ to
   lazily read the Parquet files directly from the public S3 bucket.
   No authentication is needed — the data is publicly accessible.

3. **Filter by package.** Only rows matching the requested package name(s)
   are kept.

4. **Apply additional filters.** For the ``overall`` subcommand, optional
   filters (platform, data source, version, Python version) further narrow
   the result.

5. **Aggregate.** The filtered rows are grouped and summed:

   * ``overall`` groups by ``pkg_name`` (and optionally by ``time``).
   * ``pkg_platform``, ``data_source``, ``pkg_version``, ``pkg_python``
     group by ``pkg_name`` and their respective column.

6. **Return the result.** The CLI prints the pandas result to stdout. The
   Python API returns the :class:`pandas.Series` or
   :class:`pandas.DataFrame` directly.


Performance considerations
==========================

* **Network I/O is the bottleneck.** Each query must fetch Parquet data from
  S3 over the internet. Specifying a narrow time range (``--month`` or a
  small date range) will be significantly faster than querying all data
  since 2017.

* **Dask lazy evaluation.** condastats uses Dask to construct a lazy
  computation graph and only materializes the result at the end with
  ``.compute()``. This keeps memory usage low even for large time ranges.

* **Parquet column pruning.** The groupby functions only read the columns
  they need (e.g., ``pkg_platform`` queries do not read ``pkg_version``),
  which reduces the amount of data transferred from S3.


Relationship to pypistats
==========================

condastats was inspired by `pypistats <https://pypistats.org/>`_, which
provides similar download statistics for PyPI packages. While pypistats
queries the PyPI BigQuery dataset (via the pypistats.org API), condastats
reads directly from the Anaconda S3 dataset.
