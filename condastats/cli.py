# -*- coding: utf-8 -*-

"""Console script for condastats."""
import sys
import dask.dataframe as dd
from datetime import datetime
import argparse

def load_pkg_month(package, month=None, start_month=None, end_month=None, monthly=False, pkg_platform=None, data_source=None, pkg_version=None, pkg_python=None):

    # if all optional arguments are None, read in all the data for a certain package
    df = dd.read_parquet('s3://anaconda-package-data/conda/monthly/*/*.parquet',storage_options={'anon': True})
    df = df.query(f'pkg_name in ("{package}")') 

    # if given year-month, read in data for this year-month for this package 
    if month is not None: 
        df = dd.read_parquet(f's3://anaconda-package-data/conda/monthly/{month.year}/{month.year}-{month.strftime("%m")}.parquet',
                         storage_options={'anon': True})
        df = df.query(f'pkg_name in ("{package}")')        
    
    # if given start_month and end_month, read in data between start_month and end_month
    if start_month is not None and end_month is not None:
        #read in month between start_month and end_month
        file_list = []
        for month_i in pd.period_range(start_month, end_month, freq='M'):      
            file_list.append(f's3://anaconda-package-data/conda/monthly/{month_i.year}/{month_i}.parquet')
        df = dd.read_parquet(file_list,storage_options={'anon': True})
        df = df.query(f'pkg_name in ("{package}")') 

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
        df = df.query(' and '.join(queries))
    
    # if monthly, return monthly counts
    if monthly:
        return (df.groupby('time').counts.sum().compute())
    # return sum of all counts 
    else:
        return (df.counts.sum().compute())   


def _groupby(month, package, column):
    df = dd.read_parquet(f's3://anaconda-package-data/conda/monthly/{month.year}/{month.year}-{month.strftime("%m")}.parquet',
                        columns=['pkg_name', column, 'counts'],
                        storage_options={'anon': True})
    df = df.query(f'pkg_name in ("{package}")')
    agg = df.groupby(column).counts.sum().compute()
    return agg[agg!=0]

def pkg_platform_month(month, package):
    return _groupby(month, package, 'pkg_platform')

def data_source_month(month, package):
    return _groupby(month, package, 'data_source')

def pkg_version_month(month, package):
    return _groupby(month, package, 'pkg_version')

def pkg_python_month(month, package):
    return _groupby(month, package, 'pkg_python')


def main():
    """Console script for condastats."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparserdest')

    parser_overall = subparsers.add_parser('overall')

    parser_overall.add_argument("package",
                        help="package name"
                       )

    parser_overall.add_argument("--month",
                        help="month - YYYY-MM",
                        type=lambda d: datetime.strptime(d, '%Y-%m'),
                        default=None
                       )

    parser_overall.add_argument("--start_month",
                        help="start month - YYYY-MM",
                        type=lambda d: datetime.strptime(d, '%Y-%m'),
                        default=None
                       )
 
    parser_overall.add_argument("--end_month",
                        help="end month - YYYY-MM",
                        type=lambda d: datetime.strptime(d, '%Y-%m'),
                        default=None
                       )

    parser_overall.add_argument("--monthly",
                        help="return monthly values",
                        action='store_true'
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
            package=args.package,
            month=args.month, 
            start_month=args.start_month,
            end_month = args.end_month,
            monthly=args.monthly,
            pkg_platform=args.package_platform,
            data_source=args.source,
            pkg_version=args.package_version,
            pkg_python=args.python_version
            ))
    elif args.subparserdest == 'platform':
        print(pkg_platform_month(args.month, args.package))
    elif args.subparserdest == 'source':
        print(data_source_month(args.month, args.package))
    elif args.subparserdest == 'package_version':
        print(pkg_version_month(args.month, args.package))
    elif args.subparserdest == 'python_version':
        print(pkg_python_month(args.month, args.package))


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
