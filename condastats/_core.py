"""Core functions for querying conda package download statistics."""

from __future__ import annotations

from datetime import datetime

import dask.dataframe as dd
import pandas as pd


def overall(
    package: str | list[str] | tuple[str, ...],
    month: str | datetime | None = None,
    start_month: str | datetime | None = None,
    end_month: str | datetime | None = None,
    monthly: bool = False,
    complete: bool = False,
    pkg_platform: str | None = None,
    data_source: str | None = None,
    pkg_version: str | None = None,
    pkg_python: str | float | None = None,
) -> pd.DataFrame | pd.Series:
    """Get overall download counts for one or more conda packages.

    Parameters
    ----------
    package : str or list of str
        Package name(s) to query.
    month : str or datetime, optional
        Specific month in YYYY-MM format.
    start_month : str or datetime, optional
        Start of date range in YYYY-MM format. Must be used with ``end_month``.
    end_month : str or datetime, optional
        End of date range in YYYY-MM format. Must be used with ``start_month``.
    monthly : bool, default False
        If True, return monthly breakdown instead of totals.
    complete : bool, default False
        If True, return the full DataFrame without aggregation.
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
    package_query = _normalize_package(package)
    df = _read_data(
        package_query,
        month=month,
        start_month=start_month,
        end_month=end_month,
    )

    if complete:
        df = df.compute()
        if hasattr(df["pkg_name"], "cat"):
            df["pkg_name"] = df["pkg_name"].cat.remove_unused_categories()
        return df

    # Subset data based on optional filter conditions
    queries = []
    if pkg_platform is not None:
        queries.append(f'pkg_platform in ("{pkg_platform}")')
    if data_source is not None:
        queries.append(f'data_source in ("{data_source}")')
    if pkg_version is not None:
        queries.append(f'pkg_version in ("{pkg_version}")')
    if pkg_python is not None:
        queries.append(f'pkg_python in ("{pkg_python}")')
    if queries:
        df = df.query(" and ".join(queries))

    df = df.compute()
    if hasattr(df["pkg_name"], "cat"):
        df["pkg_name"] = df["pkg_name"].cat.remove_unused_categories()

    if monthly:
        return df.groupby(["pkg_name", "time"], observed=True).counts.sum()
    else:
        return df.groupby("pkg_name", observed=True).counts.sum()


def pkg_platform(
    package: str | list[str] | tuple[str, ...],
    month: str | datetime | None = None,
    start_month: str | datetime | None = None,
    end_month: str | datetime | None = None,
    monthly: bool = False,
) -> pd.Series:
    """Get download counts grouped by platform.

    Parameters
    ----------
    package : str or list of str
        Package name(s) to query.
    month : str or datetime, optional
        Specific month in YYYY-MM format.
    start_month : str or datetime, optional
        Start of date range in YYYY-MM format.
    end_month : str or datetime, optional
        End of date range in YYYY-MM format.
    monthly : bool, default False
        If True, return monthly breakdown.

    Returns
    -------
    pandas.Series
        Download counts grouped by platform.
    """
    return _groupby(package, "pkg_platform", month, start_month, end_month, monthly)


def data_source(
    package: str | list[str] | tuple[str, ...],
    month: str | datetime | None = None,
    start_month: str | datetime | None = None,
    end_month: str | datetime | None = None,
    monthly: bool = False,
) -> pd.Series:
    """Get download counts grouped by data source.

    Parameters
    ----------
    package : str or list of str
        Package name(s) to query.
    month : str or datetime, optional
        Specific month in YYYY-MM format.
    start_month : str or datetime, optional
        Start of date range in YYYY-MM format.
    end_month : str or datetime, optional
        End of date range in YYYY-MM format.
    monthly : bool, default False
        If True, return monthly breakdown.

    Returns
    -------
    pandas.Series
        Download counts grouped by data source.
    """
    return _groupby(package, "data_source", month, start_month, end_month, monthly)


def pkg_version(
    package: str | list[str] | tuple[str, ...],
    month: str | datetime | None = None,
    start_month: str | datetime | None = None,
    end_month: str | datetime | None = None,
    monthly: bool = False,
) -> pd.Series:
    """Get download counts grouped by package version.

    Parameters
    ----------
    package : str or list of str
        Package name(s) to query.
    month : str or datetime, optional
        Specific month in YYYY-MM format.
    start_month : str or datetime, optional
        Start of date range in YYYY-MM format.
    end_month : str or datetime, optional
        End of date range in YYYY-MM format.
    monthly : bool, default False
        If True, return monthly breakdown.

    Returns
    -------
    pandas.Series
        Download counts grouped by package version.
    """
    return _groupby(package, "pkg_version", month, start_month, end_month, monthly)


def pkg_python(
    package: str | list[str] | tuple[str, ...],
    month: str | datetime | None = None,
    start_month: str | datetime | None = None,
    end_month: str | datetime | None = None,
    monthly: bool = False,
) -> pd.Series:
    """Get download counts grouped by Python version.

    Parameters
    ----------
    package : str or list of str
        Package name(s) to query.
    month : str or datetime, optional
        Specific month in YYYY-MM format.
    start_month : str or datetime, optional
        Start of date range in YYYY-MM format.
    end_month : str or datetime, optional
        End of date range in YYYY-MM format.
    monthly : bool, default False
        If True, return monthly breakdown.

    Returns
    -------
    pandas.Series
        Download counts grouped by Python version.
    """
    return _groupby(package, "pkg_python", month, start_month, end_month, monthly)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_S3_BASE = "s3://anaconda-package-data/conda/monthly"
_S3_OPTS: dict[str, bool] = {"anon": True}


def _normalize_package(
    package: str | list[str] | tuple[str, ...],
) -> str:
    """Join multiple package names into a query-safe string."""
    if isinstance(package, list | tuple):
        return '","'.join(package)
    return package


def _read_data(
    package_query: str,
    *,
    month: str | datetime | None = None,
    start_month: str | datetime | None = None,
    end_month: str | datetime | None = None,
    columns: list[str] | None = None,
) -> dd.DataFrame:
    """Read parquet data from S3 for the given time range and filter by package.

    Parameters
    ----------
    package_query : str
        Pre-normalized package name(s) for use in a query expression.
    month : str or datetime, optional
        A specific month.
    start_month : str or datetime, optional
        Start of date range.
    end_month : str or datetime, optional
        End of date range.
    columns : list, optional
        Columns to read from parquet files.

    Returns
    -------
    dask.dataframe.DataFrame
        Filtered Dask DataFrame.
    """
    read_kw: dict = dict(storage_options=_S3_OPTS, engine="pyarrow", categories=[])
    if columns:
        read_kw["columns"] = columns

    if month is not None:
        if isinstance(month, str):
            month = datetime.strptime(month, "%Y-%m")
        path = f"{_S3_BASE}/{month.year}/{month.year}-{month.strftime('%m')}.parquet"
        df = dd.read_parquet(path, **read_kw)

    elif start_month is not None and end_month is not None:
        file_list = [
            f"{_S3_BASE}/{m.year}/{m}.parquet"
            for m in pd.period_range(start_month, end_month, freq="M")
        ]
        df = dd.read_parquet(file_list, **read_kw)

    else:
        df = dd.read_parquet(f"{_S3_BASE}/*/*.parquet", **read_kw)

    return df.query(f'pkg_name in ("{package_query}")')


def _groupby(
    package: str | list[str] | tuple[str, ...],
    column: str,
    month: str | datetime | None = None,
    start_month: str | datetime | None = None,
    end_month: str | datetime | None = None,
    monthly: bool = False,
) -> pd.Series:
    """Internal helper: group download counts by a given column.

    Parameters
    ----------
    package : str or list of str
        Package name(s).
    column : str
        Column name to group by.
    month, start_month, end_month : optional
        Time range parameters.
    monthly : bool
        Whether to include a monthly breakdown.

    Returns
    -------
    pandas.Series
        Aggregated download counts.
    """
    package_query = _normalize_package(package)
    df = _read_data(
        package_query,
        month=month,
        start_month=start_month,
        end_month=end_month,
        columns=["time", "pkg_name", column, "counts"],
    )

    df = df.compute()
    if hasattr(df["pkg_name"], "cat"):
        df["pkg_name"] = df["pkg_name"].cat.remove_unused_categories()
    if hasattr(df[column], "cat"):
        df[column] = df[column].cat.remove_unused_categories()

    if monthly:
        return df.groupby(["pkg_name", "time", column], observed=True).counts.sum()
    else:
        return df.groupby(["pkg_name", column], observed=True).counts.sum()
