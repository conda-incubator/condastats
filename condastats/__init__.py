"""condastats - Query download statistics for conda packages."""

from importlib.metadata import PackageNotFoundError, version

from condastats._core import (
    data_source,
    overall,
    pkg_platform,
    pkg_python,
    pkg_version,
)

try:
    __version__ = version("condastats")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    "data_source",
    "overall",
    "pkg_platform",
    "pkg_python",
    "pkg_version",
]
