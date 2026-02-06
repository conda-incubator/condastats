.. _installation:

============
Installation
============

condastats is available from both `conda-forge <https://anaconda.org/conda-forge/condastats>`_
and `PyPI <https://pypi.org/project/condastats/>`_. Choose whichever
package manager you prefer.

.. tab-set::

   .. tab-item:: conda / mamba
      :sync: conda

      .. code-block:: console

         $ conda install -c conda-forge condastats

      Or with `mamba <https://mamba.readthedocs.io/>`_ (faster drop-in
      replacement for conda):

      .. code-block:: console

         $ mamba install -c conda-forge condastats

   .. tab-item:: pixi
      :sync: pixi

      Add condastats to a `pixi <https://pixi.sh/>`_ project:

      .. code-block:: console

         $ pixi add condastats

      Or install it as a globally available tool:

      .. code-block:: console

         $ pixi global install condastats

   .. tab-item:: pip / uv
      :sync: pip

      .. code-block:: console

         $ pip install condastats

      Or with `uv <https://docs.astral.sh/uv/>`_:

      .. code-block:: console

         $ uv pip install condastats

   .. tab-item:: pipx
      :sync: pipx

      Install as an isolated global tool with
      `pipx <https://pipx.pypa.io/>`_:

      .. code-block:: console

         $ pipx install condastats


Run without installing
======================

.. tip::

   If you just need a quick one-off query, you can run condastats in a
   temporary environment -- no permanent installation required.

.. tab-set::

   .. tab-item:: uvx

      .. code-block:: console

         $ uvx condastats overall pandas --month 2024-01

   .. tab-item:: pipx run

      .. code-block:: console

         $ pipx run condastats overall pandas --month 2024-01


Verify the installation
=======================

After installing, confirm everything works:

.. code-block:: console

   $ condastats --version

You should see the installed version number printed to the terminal.
