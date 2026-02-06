"""Core functions for querying conda package download statistics.

The public functions in this module read data from S3 via dask and delegate
the actual pandas aggregation to the pure-pandas helpers in ``_query.py``.
"""

from __future__ import annotations

from datetime import datetime

import pandas as pd

from condastats._query import query_grouped, query_overall


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
    df = _load_s3_data(
        package,
        month=month,
        start_month=start_month,
        end_month=end_month,
    )

    return query_overall(
        df,
        package=package,
        monthly=monthly,
        complete=complete,
        pkg_platform=pkg_platform,
        data_source=data_source,
        pkg_version=pkg_version,
        pkg_python=pkg_python,
    )


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
    df = _load_s3_data(
        package,
        month=month,
        start_month=start_month,
        end_month=end_month,
        columns=["time", "pkg_name", "pkg_platform", "counts"],
    )
    return query_grouped(df, "pkg_platform", package=package, monthly=monthly)


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
    df = _load_s3_data(
        package,
        month=month,
        start_month=start_month,
        end_month=end_month,
        columns=["time", "pkg_name", "data_source", "counts"],
    )
    return query_grouped(df, "data_source", package=package, monthly=monthly)


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
    df = _load_s3_data(
        package,
        month=month,
        start_month=start_month,
        end_month=end_month,
        columns=["time", "pkg_name", "pkg_version", "counts"],
    )
    return query_grouped(df, "pkg_version", package=package, monthly=monthly)


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
    df = _load_s3_data(
        package,
        month=month,
        start_month=start_month,
        end_month=end_month,
        columns=["time", "pkg_name", "pkg_python", "counts"],
    )
    return query_grouped(df, "pkg_python", package=package, monthly=monthly)


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


def _load_s3_data(
    package: str | list[str] | tuple[str, ...],
    *,
    month: str | datetime | None = None,
    start_month: str | datetime | None = None,
    end_month: str | datetime | None = None,
    columns: list[str] | None = None,
) -> pd.DataFrame:
    """Read parquet data from S3, filter by package, and return a pandas DataFrame.

    This function requires ``dask`` and ``s3fs`` to be installed.  The dask
    import is performed lazily so that ``import condastats`` succeeds even
    when dask is not available (e.g. inside Pyodide).

    Parameters
    ----------
    package : str or list of str
        Package name(s) to load data for.
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
    pandas.DataFrame
        Materialized pandas DataFrame (post-``compute()``).
    """
    import dask.dataframe as dd  # lazy import – not needed by _query.py consumers

    package_query = _normalize_package(package)

    read_kw: dict = dict(storage_options=_S3_OPTS, engine="pyarrow", categories=[])
    if columns:
        read_kw["columns"] = columns

    if month is not None:
        if isinstance(month, str):
            month = datetime.strptime(month, "%Y-%m")
        path = f"{_S3_BASE}/{month.year}/{month.year}-{month.strftime('%m')}.parquet"
        ddf = dd.read_parquet(path, **read_kw)

    elif start_month is not None and end_month is not None:
        file_list = [
            f"{_S3_BASE}/{m.year}/{m}.parquet"
            for m in pd.period_range(start_month, end_month, freq="M")
        ]
        ddf = dd.read_parquet(file_list, **read_kw)

    else:
        ddf = dd.read_parquet(f"{_S3_BASE}/*/*.parquet", **read_kw)

    ddf = ddf.query(f'pkg_name in ("{package_query}")')
    return ddf.compute()
