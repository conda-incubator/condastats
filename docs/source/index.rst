condastats
==========

A command-line tool and Python library to query download statistics for
conda packages from the `Anaconda public dataset`_.

.. code-block:: console

   $ condastats --preview pandas --month 2024-01

.. note::

   Use the flag-based preview CLI (``condastats --preview``) for both overall
   and grouped queries. The legacy subcommand path still works but now emits
   a deprecation warning; see :doc:`reference/cli` for the preview workflow and
   :doc:`reference/cli-legacy` for the older commands.

.. code-block:: python

   from condastats import overall
   overall("pandas", month="2024-01")

.. _Anaconda public dataset: https://github.com/anaconda/anaconda-package-data

Try it now
----------

Run condastats without installing -- just pick your tool:

.. tab-set::

   .. tab-item:: pixi x

      .. code-block:: console

         $ pixi x condastats --preview pandas --month 2024-01

   .. tab-item:: conda

      .. code-block:: console

         $ conda install -c conda-forge condastats
         $ condastats --preview pandas --month 2024-01

   .. tab-item:: uvx

      .. code-block:: console

         $ uvx condastats --preview pandas --month 2024-01

   .. tab-item:: pipx run

      .. code-block:: console

         $ pipx run condastats --preview pandas --month 2024-01

See :doc:`installation` for all options, or
`try it in your browser <try/>`__ -- no installation needed.

----

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: :octicon:`rocket` Getting started
      :link: tutorial
      :link-type: doc

      New to condastats? Follow the step-by-step tutorial to run your
      first download statistics query.

   .. grid-item-card:: :octicon:`globe` Try in your browser
      :link: try/

      No installation needed -- query download stats, compare packages, and
      explore charts right in your browser. Powered by Pyodide &
      WebAssembly.

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: :octicon:`download` Installation
      :link: installation
      :link-type: doc

      Install condastats via conda, mamba, pixi, pip, uv, or run it
      without installing using uvx or pipx.

   .. grid-item-card:: :octicon:`tasklist` How-to guides
      :link: howto
      :link-type: doc

      Practical recipes for filtering by time, grouping by dimension,
      comparing packages, using Jupyter, and more.

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: :octicon:`light-bulb` Explanation
      :link: explanation
      :link-type: doc

      Understand the Anaconda public dataset, how queries work
      internally, and performance considerations.

   .. grid-item-card:: :octicon:`code` Python API reference
      :link: reference/api
      :link-type: doc

      Full documentation for all public functions: ``overall``,
      ``pkg_platform``, ``data_source``, ``pkg_version``, ``pkg_python``.

.. grid:: 1
   :gutter: 3

   .. grid-item-card:: :octicon:`terminal` CLI reference
      :link: reference/cli
      :link-type: doc

      Complete documentation for the flag-based preview CLI
      (``condastats --preview``). Legacy subcommand usage is documented at
      :doc:`reference/cli-legacy`.

.. toctree::
   :hidden:

   tryit
   installation
   tutorial
   howto
   explanation
   reference/api
   reference/cli
   reference/cli-legacy
