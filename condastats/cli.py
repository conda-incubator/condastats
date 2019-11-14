# -*- coding: utf-8 -*-

"""Console script for condastats."""
import sys
import dask.dataframe as dd
from datetime import datetime
import argparse


def load_pkg_month(year, month, package, pkg_platform=None, data_source=None, pkg_version=None, pkg_python=None):
    df = dd.read_parquet(f's3://anaconda-package-data/conda/monthly/{year}/{year}-{month}.parquet',
                         storage_options={'anon': True})
    df = df.query(f'pkg_name in ("{package}")')
    
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
        df = df.query(' and '.join(queries))
        
    return (df.counts.sum().compute())

def _groupby(year, month, package, column):
    df = dd.read_parquet(f's3://anaconda-package-data/conda/monthly/{year}/{year}-{month}.parquet',
                        columns=['pkg_name', column, 'counts'],
                        storage_options={'anon': True})
    df = df.query(f'pkg_name in ("{package}")')
    agg = df.groupby(column).counts.sum().compute()
    return agg[agg!=0]

def pkg_platform_month(year, month, package):
    return _groupby(year, month, package, 'pkg_platform')

def data_source_month(year, month, package):
    return _groupby(year, month, package, 'data_source')

def pkg_version_month(year, month, package):
    return _groupby(year, month, package, 'pkg_version')

def pkg_python_month(year, month, package):
    return _groupby(year, month, package, 'pkg_python')


def main():
    """Console script for condastats."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparserdest')

    parser_overall = subparsers.add_parser('overall')

    parser_overall.add_argument("package",
                        help="package name"
                       )

    parser_overall.add_argument("month",
                        help="month - YYYY-MM",
                        type=lambda d: datetime.strptime(d, '%Y-%m')
                       )
    
    parser_overall.add_argument("--package_platform",
                        help="package platform e.g., win-64, linux-32, osx-64.",
                        default=None 
                       )
    
    parser_overall.add_argument("--python_version",
                        help="Python version e.g., 3.7",
                        default=None 
                       )
     
    parser_overall.add_argument("--package_version",
                        help="Python version e.g., 0.1.0",
                        default=None 
                       )   
    parser_overall.add_argument("--source",
                        help="Data source e.g., anaconda, conda-forge",
                        default=None 
                       )  

    parser_platform = subparsers.add_parser('platform')

    parser_platform.add_argument("package",
                        help="package name"
                       )

    parser_platform.add_argument("month",
                        help="month - YYYY-MM",
                        type=lambda d: datetime.strptime(d, '%Y-%m')
                       )

    parser_source = subparsers.add_parser('source')

    parser_source.add_argument("package",
                        help="package name"
                       )

    parser_source.add_argument("month",
                        help="month - YYYY-MM",
                        type=lambda d: datetime.strptime(d, '%Y-%m')
                       )
    parser_package_version = subparsers.add_parser('package_version')

    parser_package_version.add_argument("package",
                        help="package name"
                       )

    parser_package_version.add_argument("month",
                        help="month - YYYY-MM",
                        type=lambda d: datetime.strptime(d, '%Y-%m')
                       )
    
    parser_python_version = subparsers.add_parser('python_version')

    parser_python_version.add_argument("package",
                        help="package name"
                       )

    parser_python_version.add_argument("month",
                        help="month - YYYY-MM",
                        type=lambda d: datetime.strptime(d, '%Y-%m')
                       )
    args = parser.parse_args()

    if args.subparserdest == 'overall':
        print(load_pkg_month(
            year=args.month.year, 
            month=args.month.strftime('%m'), 
            package=args.package,
            pkg_platform=args.package_platform,
            data_source=args.source,
            pkg_version=args.package_version,
            pkg_python=args.python_version
            ))
    elif args.subparserdest == 'platform':
        print(pkg_platform_month(args.month.year, args.month.strftime('%m'), args.package))
    elif args.subparserdest == 'source':
        print(data_source_month(args.month.year, args.month.strftime('%m'), args.package))
    elif args.subparserdest == 'package_version':
        print(pkg_version_month(args.month.year, args.month.strftime('%m'), args.package))
    elif args.subparserdest == 'python_version':
        print(pkg_python_month(args.month.year, args.month.strftime('%m'), args.package))


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
