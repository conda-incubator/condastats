.. highlight:: shell

============
Installation
============

Using conda / mamba / pixi (recommended)
-----------------------------------------

.. code-block:: console

    $ conda install -c conda-forge condastats

Or with `mamba <https://mamba.readthedocs.io/>`__ (faster drop-in replacement for conda):

.. code-block:: console

    $ mamba install -c conda-forge condastats

Or with `pixi <https://pixi.sh/>`__:

.. code-block:: console

    $ pixi add condastats

To install ``condastats`` as a globally available tool with pixi:

.. code-block:: console

    $ pixi global install condastats

Using pip / uv
--------------

.. code-block:: console

    $ pip install condastats

Or with `uv <https://docs.astral.sh/uv/>`__:

.. code-block:: console

    $ uv pip install condastats

To run ``condastats`` without installing, use
`uvx <https://docs.astral.sh/uv/guides/tools/>`__ or
`pipx run <https://pipx.pypa.io/>`__:

.. code-block:: console

    $ uvx condastats overall pandas --month 2024-01
    $ pipx run condastats overall pandas --month 2024-01

Or install as a global tool with `pipx <https://pipx.pypa.io/>`__:

.. code-block:: console

    $ pipx install condastats


.. _Github repo: https://github.com/conda-incubator/condastats
