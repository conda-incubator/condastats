# -*- coding: utf-8 -*-

"""Console script for condastats."""
import argparse
import sys
from datetime import datetime
from typing import List, Optional, Tuple, Union

import dask.dataframe as dd
import pandas as pd

pd.set_option("display.max_rows", None)


def overall(
    package: Union[str, List[str], Tuple[str, ...]],
    month: Optional[Union[str, datetime]] = None,
    start_month: Optional[Union[str, datetime]] = None,
    end_month: Optional[Union[str, datetime]] = None,
    monthly: bool = False,
    complete: bool = False,
    pkg_platform: Optional[str] = None,
    data_source: Optional[str] = None,
    pkg_version: Optional[str] = None,
    pkg_python: Optional[Union[str, float]] = None,
) -> Union[pd.DataFrame, pd.Series]:

    # so we can pass in one or more packages
    # if more than one packages, e.g., ("pandas","dask") as a tuple or
    # ["pandas","dask"] as a list,we need to them with "," so that in
    # f-string it can read correctly as pkg_name in ("pandas","dask")
    if isinstance(package, tuple) or isinstance(package, list):
        package = '","'.join(package)

    # if given year-month, read in data for this year-month for this package
    if month is not None:
        # if month is string, we change the type to datetime.
        if isinstance(month, str):
            month = datetime.strptime(month, "%Y-%m")
        df = dd.read_parquet(
            f's3://anaconda-package-data/conda/monthly/{month.year}/{month.year}-{month.strftime("%m")}.parquet',
            storage_options={"anon": True},
            engine="pyarrow",
            categories=[],
        )
        df = df.query(f'pkg_name in ("{package}")')

    # if given start_month and end_month, read in data
    # between start_month and end_month
    elif start_month is not None and end_month is not None:
        # read in month between start_month and end_month
        file_list = []
        for month_i in pd.period_range(start_month, end_month, freq="M"):
            file_list.append(
                f"s3://anaconda-package-data/conda/monthly/{month_i.year}/{month_i}.parquet"
            )
        df = dd.read_parquet(file_list, storage_options={"anon": True}, engine="pyarrow", categories=[])
        df = df.query(f'pkg_name in ("{package}")')

    # if all optional arguments are None, read in all
    # the data for a certain package
    else:
        # if all optional arguments are None, read in
        # all the data for a certain package
        df = dd.read_parquet(
            "s3://anaconda-package-data/conda/monthly/*/*.parquet",
            storage_options={"anon": True},
            engine="pyarrow",
            categories=[],
        )
        df = df.query(f'pkg_name in ("{package}")')

    if complete:
        df = df.compute()
        if hasattr(df["pkg_name"], "cat"):
            df["pkg_name"] = df["pkg_name"].cat.remove_unused_categories()
        return df

    # subset data based on other conditions if given
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

    # if monthly, return monthly counts
    if monthly:
        monthly_counts = df.groupby(["pkg_name", "time"], observed=True).counts.sum()
        return monthly_counts
    # return sum of all counts
    else:
        total_counts = df.groupby("pkg_name", observed=True).counts.sum()
        return total_counts


def _groupby(
    package: Union[str, List[str], Tuple[str, ...]],
    column: str,
    month: Optional[Union[str, datetime]] = None,
    start_month: Optional[Union[str, datetime]] = None,
    end_month: Optional[Union[str, datetime]] = None,
    monthly: bool = False,
) -> pd.Series:

    if isinstance(package, tuple) or isinstance(package, list):
        package = '","'.join(package)

    # if given year-month, read in data for this year-month for this package
    if month is not None:
        if isinstance(month, str):
            month = datetime.strptime(month, "%Y-%m")
        df = dd.read_parquet(
            f's3://anaconda-package-data/conda/monthly/{month.year}/{month.year}-{month.strftime("%m")}.parquet',
            columns=["time", "pkg_name", column, "counts"],
            storage_options={"anon": True},
            engine="pyarrow",
            categories=[],
        )
        df = df.query(f'pkg_name in ("{package}")')

    # if given start_month and end_month, read in data
    # between start_month and end_month
    elif start_month is not None and end_month is not None:
        # read in month between start_month and end_month
        file_list = []
        for month_i in pd.period_range(start_month, end_month, freq="M"):
            file_list.append(
                f"s3://anaconda-package-data/conda/monthly/{month_i.year}/{month_i}.parquet"
            )
        df = dd.read_parquet(
            file_list,
            columns=["time", "pkg_name", column, "counts"],
            storage_options={"anon": True},
            engine="pyarrow",
            categories=[],
        )
        df = df.query(f'pkg_name in ("{package}")')

    # if all optional arguments are None, read in all the
    # data for a certain package
    else:
        df = dd.read_parquet(
            f"s3://anaconda-package-data/conda/monthly/*/*.parquet",
            columns=["time", "pkg_name", column, "counts"],
            storage_options={"anon": True},
            engine="pyarrow",
            categories=[],
        )
        df = df.query(f'pkg_name in ("{package}")')

    df = df.compute()
    if hasattr(df["pkg_name"], "cat"):
        df["pkg_name"] = df["pkg_name"].cat.remove_unused_categories()
    if hasattr(df[column], "cat"):
        df[column] = df[column].cat.remove_unused_categories()

    # if monthly, return monthly counts
    if monthly:
        agg = df.groupby(["pkg_name", "time", column], observed=True).counts.sum()
    # return sum of all counts
    else:
        agg = df.groupby(["pkg_name", column], observed=True).counts.sum()

    return agg


def pkg_platform(
    package: Union[str, List[str], Tuple[str, ...]],
    month: Optional[Union[str, datetime]] = None,
    start_month: Optional[Union[str, datetime]] = None,
    end_month: Optional[Union[str, datetime]] = None,
    monthly: bool = False,
) -> pd.Series:
    return _groupby(
        package, "pkg_platform", month, start_month, end_month, monthly
    )


def data_source(
    package: Union[str, List[str], Tuple[str, ...]],
    month: Optional[Union[str, datetime]] = None,
    start_month: Optional[Union[str, datetime]] = None,
    end_month: Optional[Union[str, datetime]] = None,
    monthly: bool = False,
) -> pd.Series:
    return _groupby(
        package, "data_source", month, start_month, end_month, monthly
    )


def pkg_version(
    package: Union[str, List[str], Tuple[str, ...]],
    month: Optional[Union[str, datetime]] = None,
    start_month: Optional[Union[str, datetime]] = None,
    end_month: Optional[Union[str, datetime]] = None,
    monthly: bool = False,
) -> pd.Series:
    return _groupby(
        package, "pkg_version", month, start_month, end_month, monthly
    )


def pkg_python(
    package: Union[str, List[str], Tuple[str, ...]],
    month: Optional[Union[str, datetime]] = None,
    start_month: Optional[Union[str, datetime]] = None,
    end_month: Optional[Union[str, datetime]] = None,
    monthly: bool = False,
) -> pd.Series:
    return _groupby(
        package, "pkg_python", month, start_month, end_month, monthly
    )


def main():
    """Console script for condastats."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparserdest")

    parser_overall = subparsers.add_parser("overall")

    parser_overall.add_argument("package", help="package name(s)", nargs="+")

    parser_overall.add_argument(
        "--month",
        help="month - YYYY-MM (default: None)",
        type=lambda d: datetime.strptime(d, "%Y-%m"),
        default=None,
    )

    parser_overall.add_argument(
        "--start_month",
        help="start month - YYYY-MM (default: None)",
        type=lambda d: datetime.strptime(d, "%Y-%m"),
        default=None,
    )

    parser_overall.add_argument(
        "--end_month",
        help="end month - YYYY-MM (default: None)",
        type=lambda d: datetime.strptime(d, "%Y-%m"),
        default=None,
    )

    parser_overall.add_argument(
        "--monthly",
        help="return monthly values (default: False)",
        action="store_true",
    )

    parser_overall.add_argument(
        "--complete",
        help="return all values (default: False)",
        action="store_true",
    )

    parser_overall.add_argument(
        "--pkg_platform",
        help="package platform e.g., win-64, linux-32, osx-64. (default: None)",
        default=None,
    )

    parser_overall.add_argument(
        "--pkg_python",
        help="Python version e.g., 3.7 (default: None)",
        default=None,
    )

    parser_overall.add_argument(
        "--pkg_version",
        help="Python version e.g., 0.1.0 (default: None)",
        default=None,
    )
    parser_overall.add_argument(
        "--data_source",
        help="Data source e.g., anaconda, conda-forge (default: None)",
        default=None,
    )

    parser_platform = subparsers.add_parser("pkg_platform")

    parser_platform.add_argument("package", help="package name(s)", nargs="+")

    parser_platform.add_argument(
        "--month",
        help="month - YYYY-MM (default: None)",
        type=lambda d: datetime.strptime(d, "%Y-%m"),
        default=None,
    )

    parser_platform.add_argument(
        "--start_month",
        help="start month - YYYY-MM (default: None)",
        type=lambda d: datetime.strptime(d, "%Y-%m"),
        default=None,
    )

    parser_platform.add_argument(
        "--end_month",
        help="end month - YYYY-MM (default: None)",
        type=lambda d: datetime.strptime(d, "%Y-%m"),
        default=None,
    )

    parser_platform.add_argument(
        "--monthly",
        help="return monthly values (default: False)",
        action="store_true",
    )

    parser_source = subparsers.add_parser("data_source")

    parser_source.add_argument("package", help="package name(s)", nargs="+")

    parser_source.add_argument(
        "--month",
        help="month - YYYY-MM (default: None)",
        type=lambda d: datetime.strptime(d, "%Y-%m"),
        default=None,
    )
    parser_source.add_argument(
        "--start_month",
        help="start month - YYYY-MM (default: None)",
        type=lambda d: datetime.strptime(d, "%Y-%m"),
        default=None,
    )

    parser_source.add_argument(
        "--end_month",
        help="end month - YYYY-MM (default: None)",
        type=lambda d: datetime.strptime(d, "%Y-%m"),
        default=None,
    )

    parser_source.add_argument(
        "--monthly",
        help="return monthly values (default: False)",
        action="store_true",
    )

    parser_package_version = subparsers.add_parser("pkg_version")

    parser_package_version.add_argument(
        "package", help="package name(s)", nargs="+"
    )

    parser_package_version.add_argument(
        "--month",
        help="month - YYYY-MM (default: None)",
        type=lambda d: datetime.strptime(d, "%Y-%m"),
        default=None,
    )
    parser_package_version.add_argument(
        "--start_month",
        help="start month - YYYY-MM (default: None)",
        type=lambda d: datetime.strptime(d, "%Y-%m"),
        default=None,
    )

    parser_package_version.add_argument(
        "--end_month",
        help="end month - YYYY-MM (default: None)",
        type=lambda d: datetime.strptime(d, "%Y-%m"),
        default=None,
    )

    parser_package_version.add_argument(
        "--monthly",
        help="return monthly values (default: False)",
        action="store_true",
    )

    parser_python_version = subparsers.add_parser("pkg_python")

    parser_python_version.add_argument(
        "package", help="package name(s)", nargs="+"
    )

    parser_python_version.add_argument(
        "--month",
        help="month - YYYY-MM (default: None)",
        type=lambda d: datetime.strptime(d, "%Y-%m"),
        default=None,
    )
    parser_python_version.add_argument(
        "--start_month",
        help="start month - YYYY-MM (default: None)",
        type=lambda d: datetime.strptime(d, "%Y-%m"),
        default=None,
    )

    parser_python_version.add_argument(
        "--end_month",
        help="end month - YYYY-MM (default: None)",
        type=lambda d: datetime.strptime(d, "%Y-%m"),
        default=None,
    )

    parser_python_version.add_argument(
        "--monthly",
        help="return monthly values (default: False)",
        action="store_true",
    )

    args = parser.parse_args()

    if args.subparserdest == "overall":
        print(
            overall(
                package=args.package,
                month=args.month,
                complete=args.complete,
                start_month=args.start_month,
                end_month=args.end_month,
                monthly=args.monthly,
                pkg_platform=args.pkg_platform,
                data_source=args.data_source,
                pkg_version=args.pkg_version,
                pkg_python=args.pkg_python,
            )
        )
    elif args.subparserdest == "pkg_platform":
        print(
            pkg_platform(
                package=args.package,
                month=args.month,
                start_month=args.start_month,
                end_month=args.end_month,
                monthly=args.monthly,
            )
        )
    elif args.subparserdest == "data_source":
        print(
            data_source(
                package=args.package,
                month=args.month,
                start_month=args.start_month,
                end_month=args.end_month,
                monthly=args.monthly,
            )
        )
    elif args.subparserdest == "pkg_version":
        print(
            pkg_version(
                package=args.package,
                month=args.month,
                start_month=args.start_month,
                end_month=args.end_month,
                monthly=args.monthly,
            )
        )
    elif args.subparserdest == "pkg_python":
        print(
            pkg_python(
                package=args.package,
                month=args.month,
                start_month=args.start_month,
                end_month=args.end_month,
                monthly=args.monthly,
            )
        )


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
