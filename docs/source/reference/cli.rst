.. _cli-reference:

======================
Command-line interface
======================

condastats now routes CLI requests through a flag-based preview entry point
when ``--preview`` appears before the packages. This syntax mirrors the
existing functions and grouping dimensions while keeping the legacy
subcommand path for backward compatibility (the legacy path emits a
deprecation warning). The flag-based preview CLI is documented here; see
:doc:`cli-legacy` for the older subcommand interface.

General usage
=============

The preview CLI uses a package-first syntax with optional filters:

.. code-block:: console

   $ condastats --preview pandas --month 2024-01
   $ condastats --preview --group pkg_platform pandas --month 2024-01
   $ condastats --preview pandas numpy --month 2024-01 --pkg_platform linux-64

``--preview``
   Route execution to the flag-based preview parser. This flag must appear
   before the first package name.

``--version``
   Print the installed ``condastats`` version and exit.

``--help``
   Show the help message and exit.

Routing behavior
================

.. mermaid::

   flowchart TB
       root["condastats [--preview] [--version] ..."]
       root --> router["command router"]
       router --> decision{"--preview present?"}
       decision -->|No| legacy["Subcommand path"]
       decision -->|Yes| preview["Preview path"]
       legacy --> warn["Emit deprecation warning with preview hint"]
       legacy --> dispatch["Parse, validate, and dispatch subcommands"]
       preview --> strip["Remove --preview before handling preview args"]
       strip --> preview_exec["Parse flag-based args and dispatch supported queries"]

Preview usage
=============

The preview path supports two kinds of queries:

- **Overall queries** (the default). You can apply the full suite of filter
  flags: ``--complete``, ``--pkg_platform``, ``--data_source``,
  ``--pkg_version``, and ``--pkg_python``.
- **Grouped queries**. Supply a single ``--group`` value to replace the
  grouping subcommand. Grouped queries currently only accept the common time
  filters (``--month``, ``--start_month``, ``--end_month``, ``--monthly``)
  and do *not* accept ``--complete`` or the overall-only filters.

Grouped preview queries intentionally keep the same output as the legacy
subcommands; in other words, ``condastats --preview --group pkg_platform`` is
behaviorally identical to the old ``condastats pkg_platform`` invocation,
just with a different syntax.

Preview queries always expect at least one package. Multiple packages remain
space-separated, just like the legacy CLI.

Common options
==============

.. _cli-common-options:

These options apply to **every** preview query:

``package``
   **Required.** One or more package names. Multiple names are space-separated.

``--month YYYY-MM``
   Restrict results to a single month. Cannot be used together with
   ``--start_month``/``--end_month``.

``--start_month YYYY-MM``
   Start of a date range (inclusive). Must be combined with ``--end_month``.

``--end_month YYYY-MM``
   End of a date range (inclusive). Must be combined with ``--start_month``.

``--monthly``
   Return per-month counts instead of a single total. Most useful with a date
   range.

Overall query filters
=====================

When ``--group`` is omitted, the preview CLI calls :func:`~condastats.overall`
and supports the additional filters listed below:

``--complete``
   Return every row instead of aggregated counts.

``--pkg_platform PLATFORM``
   Limit results to a single platform (e.g., ``linux-64``, ``osx-arm64``,
   ``win-64``).

``--data_source SOURCE``
   Limit results to a specific channel or repository (e.g., ``anaconda``,
   ``conda-forge``).

``--pkg_version VERSION``
   Limit results to a precise package version (e.g., ``1.5.3``).

``--pkg_python VERSION``
   Limit results to a Python version (e.g., ``3.11``).

Grouped queries
===============

Use ``--group`` to ask for a dimensionally grouped result. Each supported value
corresponds to a legacy grouping subcommand:

- ``pkg_platform``: group by ``pkg_platform`` (platform architecture).
- ``data_source``: group by ``data_source`` (channel).
- ``pkg_version``: group by ``pkg_version`` (package version).
- ``pkg_python``: group by ``pkg_python`` (Python version built for).

.. code-block:: console

   $ condastats --preview --group data_source pandas --month 2024-01

Grouped queries only respect the common time filters listed above and cannot
combine with ``--complete`` or the overall-only filters.

Legacy subcommand reference
===========================

The legacy subcommand interface still works and is documented in
:doc:`cli-legacy`, but it emits a deprecation warning and will be
removed after the preview syntax matures.

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
