"""condastats - Query download statistics for conda packages."""

from importlib.metadata import PackageNotFoundError, version

# S3-backed convenience functions – require dask & s3fs at *call* time.
# The dask import inside _core is lazy, so this import always succeeds;
# the functions simply raise ImportError when actually called without dask.
from condastats._core import (
    data_source,
    overall,
    pkg_platform,
    pkg_python,
    pkg_version,
)

# Pure-pandas query functions – always available (only need pandas).
from condastats._query import (
    query_grouped,
    query_overall,
    top_packages,
)

try:
    __version__ = version("condastats")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    # Pure-pandas query API (works everywhere, including Pyodide)
    "query_grouped",
    "query_overall",
    "top_packages",
    # S3-backed convenience API (requires dask + s3fs)
    "data_source",
    "overall",
    "pkg_platform",
    "pkg_python",
    "pkg_version",
]
