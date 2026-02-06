.. _cli-reference:

======================
Command-line interface
======================

condastats provides a ``condastats`` command with several subcommands for
querying package download statistics.


General usage
=============

.. code-block:: console

   $ condastats [--version] [--help] <subcommand> [options] package [package ...]

``--version``
   Print the installed condastats version and exit.

``--help``
   Show the help message and exit.


Subcommands
===========

overall
-------

Return aggregate download counts, optionally filtered by platform, data
source, package version, or Python version.

.. code-block:: console

   $ condastats overall [options] package [package ...]

Options (in addition to the :ref:`common options <cli-common-options>`):

``--complete``
   Return all rows from the dataset instead of aggregated counts.

``--pkg_platform PLATFORM``
   Filter by platform (e.g., ``linux-64``, ``osx-arm64``, ``win-64``).

``--data_source SOURCE``
   Filter by data source (e.g., ``anaconda``, ``conda-forge``).

``--pkg_version VERSION``
   Filter by package version (e.g., ``1.5.3``).

``--pkg_python VERSION``
   Filter by Python version (e.g., ``3.11``).

**Examples:**

.. code-block:: console

   $ condastats overall pandas
   $ condastats overall pandas --month 2024-01
   $ condastats overall pandas --month 2024-01 --pkg_platform linux-64
   $ condastats overall pandas numpy dask --start_month 2024-01 --end_month 2024-06 --monthly


pkg_platform
------------

Return download counts grouped by platform.

.. code-block:: console

   $ condastats pkg_platform [options] package [package ...]

**Example:**

.. code-block:: console

   $ condastats pkg_platform pandas --month 2024-01


data_source
-----------

Return download counts grouped by data source (channel).

.. code-block:: console

   $ condastats data_source [options] package [package ...]

**Example:**

.. code-block:: console

   $ condastats data_source pandas --month 2024-01


pkg_version
-----------

Return download counts grouped by package version.

.. code-block:: console

   $ condastats pkg_version [options] package [package ...]

**Example:**

.. code-block:: console

   $ condastats pkg_version pandas --month 2024-01


pkg_python
----------

Return download counts grouped by Python version.

.. code-block:: console

   $ condastats pkg_python [options] package [package ...]

**Example:**

.. code-block:: console

   $ condastats pkg_python pandas --month 2024-01


.. _cli-common-options:

Common options
==============

These options are available on **every** subcommand:

``package``
   **Required.** One or more package names. Multiple names are
   space-separated.

``--month YYYY-MM``
   Restrict results to a single month. Cannot be used together with
   ``--start_month``/``--end_month``.

``--start_month YYYY-MM``
   Start of a date range (inclusive). Must be combined with ``--end_month``.

``--end_month YYYY-MM``
   End of a date range (inclusive). Must be combined with ``--start_month``.

``--monthly``
   Return per-month counts instead of a single total. Most useful with a
   date range.


Exit codes
==========

.. list-table::
   :header-rows: 1

   * - Code
     - Meaning
   * - 0
     - Success
   * - 2
     - Invalid arguments (missing subcommand, bad option combination, etc.)
