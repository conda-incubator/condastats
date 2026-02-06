.. _tryit:

=======================
Try it in your browser
=======================

No installation needed -- run condastats queries directly in your browser.
The interactive demo uses `Pyodide <https://pyodide.org/>`_ to run Python,
pandas, and fastparquet entirely in WebAssembly. Download data, query
packages, compare statistics, and explore charts -- all client-side.

.. raw:: html

   <a href="../try/"
      style="display:inline-block;padding:0.7rem 1.5rem;font-size:1.05rem;
             font-weight:600;color:#fff;background:#348721;border-radius:6px;
             text-decoration:none;margin:0.5rem 0 1.5rem;"
      onmouseover="this.style.background='#2f7a1e'"
      onmouseout="this.style.background='#348721'">
     Open interactive demo &rarr;
   </a>

.. note::

   Each month's data (1--15 MB) is downloaded on demand and cached in
   your browser. You can query single months or multi-month ranges.
   For full programmatic access, :doc:`install condastats locally
   <installation>`.
