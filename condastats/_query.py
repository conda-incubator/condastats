"""Pure-pandas query functions for conda download statistics.

These functions operate on pre-loaded pandas DataFrames and have no
dependency on dask, s3fs, or any I/O layer.  They are used internally
by the S3-backed public API in ``_core.py`` and can also be called
directly when data has been loaded through other means (e.g. Pyodide).
"""

from __future__ import annotations

import pandas as pd


def query_overall(
    df: pd.DataFrame,
    package: str | list[str] | tuple[str, ...] | None = None,
    monthly: bool = False,
    complete: bool = False,
    pkg_platform: str | None = None,
    data_source: str | None = None,
    pkg_version: str | None = None,
    pkg_python: str | float | None = None,
) -> pd.DataFrame | pd.Series:
    """Get overall download counts from a pandas DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with at least ``pkg_name`` and ``counts`` columns.
    package : str or list of str, optional
        Package name(s) to filter by.  If *None*, all packages are included.
    monthly : bool, default False
        If True, return monthly breakdown instead of totals.
    complete : bool, default False
        If True, return the full filtered DataFrame without aggregation.
    pkg_platform : str, optional
        Filter by platform (e.g., 'linux-64', 'osx-64', 'win-64').
    data_source : str, optional
        Filter by data source (e.g., 'anaconda', 'conda-forge').
    pkg_version : str, optional
        Filter by package version.
    pkg_python : str or float, optional
        Filter by Python version (e.g., '3.7' or 3.7).

    Returns
    -------
    pandas.Series or pandas.DataFrame
        Download counts, either as a Series (aggregated) or DataFrame (complete).
    """
    df = _filter_packages(df, package)

    # Apply optional dimension filters
    conditions = []
    if pkg_platform is not None:
        conditions.append(df["pkg_platform"] == pkg_platform)
    if data_source is not None:
        conditions.append(df["data_source"] == data_source)
    if pkg_version is not None:
        conditions.append(df["pkg_version"] == pkg_version)
    if pkg_python is not None:
        conditions.append(df["pkg_python"] == str(pkg_python))

    if conditions:
        mask = conditions[0]
        for c in conditions[1:]:
            mask = mask & c
        df = df[mask]

    df = _clean_categories(df, "pkg_name")

    if complete:
        return df

    if monthly:
        return df.groupby(["pkg_name", "time"], observed=True)["counts"].sum()
    return df.groupby("pkg_name", observed=True)["counts"].sum()


def query_grouped(
    df: pd.DataFrame,
    column: str,
    package: str | list[str] | tuple[str, ...] | None = None,
    monthly: bool = False,
) -> pd.Series:
    """Get download counts grouped by a given dimension.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with ``pkg_name``, ``counts``, and *column* columns.
    column : str
        Column name to group by (e.g., ``'pkg_platform'``, ``'data_source'``).
    package : str or list of str, optional
        Package name(s) to filter by.  If *None*, all packages are included.
    monthly : bool, default False
        If True, include a monthly breakdown.

    Returns
    -------
    pandas.Series
        Aggregated download counts.
    """
    df = _filter_packages(df, package)
    df = _clean_categories(df, "pkg_name")
    df = _clean_categories(df, column)

    if monthly:
        return df.groupby(["pkg_name", "time", column], observed=True)["counts"].sum()
    return df.groupby(["pkg_name", column], observed=True)["counts"].sum()


def top_packages(
    df: pd.DataFrame,
    n: int = 20,
) -> pd.Series:
    """Get the top *n* most downloaded packages.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with ``pkg_name`` and ``counts`` columns.
    n : int, default 20
        Number of top packages to return.

    Returns
    -------
    pandas.Series
        Top *n* packages sorted by total downloads (descending).
    """
    return (
        df.groupby("pkg_name", observed=True)["counts"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _filter_packages(
    df: pd.DataFrame,
    package: str | list[str] | tuple[str, ...] | None,
) -> pd.DataFrame:
    """Filter DataFrame to the requested package(s)."""
    if package is None:
        return df
    if isinstance(package, str):
        package = [package]
    return df[df["pkg_name"].isin(package)]


def _clean_categories(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Remove unused categories from a column, if categorical."""
    if hasattr(df[column], "cat"):
        df = df.copy()
        df[column] = df[column].cat.remove_unused_categories()
    return df
