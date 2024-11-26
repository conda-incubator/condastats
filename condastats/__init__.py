# -*- coding: utf-8 -*-

"""Top-level package for condastats."""

__author__ = """Sophia Man Yang"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("condastats")
except PackageNotFoundError:
    # package is not installed
    pass
