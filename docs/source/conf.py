# Configuration file for the Sphinx documentation builder.
#
# Full list of options: https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from importlib.metadata import version as get_version

sys.path.insert(0, os.path.abspath("."))

# -- Project information -----------------------------------------------------

project = html_title = "condastats"
copyright = "2019-2026, Sophia Man Yang"
author = "Sophia Man Yang"

release: str = get_version("condastats")
version: str = ".".join(release.split(".")[:2])

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
]

source_suffix = ".rst"
master_doc = "index"
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

html_theme = "conda_sphinx_theme"

html_static_path = []
htmlhelp_basename = "condastatsdoc"

html_theme_options = {
    "navigation_depth": -1,
    "use_edit_page_button": True,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/conda-incubator/condastats",
            "icon": "fa-brands fa-square-github",
            "type": "fontawesome",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/condastats/",
            "icon": "fa-brands fa-python",
            "type": "fontawesome",
        },
        {
            "name": "conda-forge",
            "url": "https://anaconda.org/conda-forge/condastats",
            "icon": "fa-solid fa-cube",
            "type": "fontawesome",
        },
    ],
}

html_context = {
    "github_user": "conda-incubator",
    "github_repo": "condastats",
    "github_version": "main",
    "doc_path": "docs/source",
}

# -- Intersphinx -------------------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
    "dask": ("https://docs.dask.org/en/stable", None),
}

# -- Autodoc -----------------------------------------------------------------

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

autodoc_member_order = "groupwise"
autodoc_mock_imports = ["snappy"]
autodoc_typehints = "description"

# -- Copy button -------------------------------------------------------------

copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True

# -- LaTeX output ------------------------------------------------------------

latex_documents = [
    (
        master_doc,
        "condastats.tex",
        "condastats Documentation",
        "Sophia Man Yang",
        "manual",
    ),
]

# -- Manual page output ------------------------------------------------------

man_pages = [(master_doc, "condastats", "condastats Documentation", [author], 1)]

# -- Texinfo output ----------------------------------------------------------

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
