.. _installation:

============
Installation
============

condastats is available from both `conda-forge <https://anaconda.org/conda-forge/condastats>`_
and `PyPI <https://pypi.org/project/condastats/>`_. Choose whichever
package manager you prefer.


.. contents::
   :local:
   :depth: 1


Using conda / mamba (recommended)
=================================

.. code-block:: console

   $ conda install -c conda-forge condastats

Or with `mamba <https://mamba.readthedocs.io/>`_ (faster drop-in
replacement for conda):

.. code-block:: console

   $ mamba install -c conda-forge condastats


Using pixi
===========

Add condastats to a `pixi <https://pixi.sh/>`_ project:

.. code-block:: console

   $ pixi add condastats

Or install it as a globally available tool:

.. code-block:: console

   $ pixi global install condastats


Using pip / uv
==============

.. code-block:: console

   $ pip install condastats

Or with `uv <https://docs.astral.sh/uv/>`_:

.. code-block:: console

   $ uv pip install condastats


Run without installing
======================

If you just need a quick one-off query, you can run condastats in a
temporary environment using `uvx <https://docs.astral.sh/uv/guides/tools/>`_,
`pipx run <https://pipx.pypa.io/>`_, or `pixi exec <https://pixi.sh/>`_:

.. code-block:: console

   $ uvx condastats overall pandas --month 2024-01
   $ pipx run condastats overall pandas --month 2024-01

These download condastats into a temporary environment, run the command, and
clean up afterwards — no permanent installation required.


Install as a global CLI tool
============================

Use `pipx <https://pipx.pypa.io/>`_ or ``pixi global`` to install
condastats into its own isolated environment while making the ``condastats``
command available system-wide:

.. code-block:: console

   $ pipx install condastats
   $ pixi global install condastats


Verify the installation
=======================

After installing, confirm everything works:

.. code-block:: console

   $ condastats --version

You should see the installed version number printed to the terminal.
