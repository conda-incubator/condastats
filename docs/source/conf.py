# Configuration file for the Sphinx documentation builder.
#
# Full list of options: https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from importlib.metadata import version as get_version

sys.path.insert(0, os.path.abspath("."))

# -- Project information -----------------------------------------------------

project = "condastats"
copyright = "2019-2026, Sophia Man Yang"
author = "Sophia Man Yang"

release: str = get_version("condastats")
version: str = ".".join(release.split(".")[:2])

# -- General configuration ---------------------------------------------------

extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode"]

source_suffix = ".rst"
master_doc = "index"
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

html_theme = "conda_sphinx_theme"

html_static_path = ["_static"]
htmlhelp_basename = "condastatsdoc"

# -- Options for LaTeX output ------------------------------------------------

latex_documents = [
    (
        master_doc,
        "condastats.tex",
        "condastats Documentation",
        "Sophia Man Yang",
        "manual",
    ),
]

# -- Options for manual page output ------------------------------------------

man_pages = [(master_doc, "condastats", "condastats Documentation", [author], 1)]

# -- Options for Texinfo output ----------------------------------------------

texinfo_documents = [
    (
        master_doc,
        "condastats",
        "condastats Documentation",
        author,
        "condastats",
        "Query download statistics for conda packages.",
        "Miscellaneous",
    ),
]

# -- Autodoc -----------------------------------------------------------------

autodoc_default_options = {
    "undoc-members": None,
}

autodoc_member_order = "groupwise"
autodoc_mock_imports = ["snappy"]
