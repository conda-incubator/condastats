# -*- coding: utf-8 -*-

"""Top-level package for condastats."""

from importlib.metadata import version, PackageNotFoundError

__author__ = """Sophia Man Yang"""

try:
    __version__ = version("condastats")
except PackageNotFoundError:
    __version__ = "0.0.0"
