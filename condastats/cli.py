# -*- coding: utf-8 -*-

"""Console script for condastats."""
import sys
import dask.dataframe as dd
import pandas as pd
from datetime import datetime
import argparse
pd.set_option('display.max_rows', None)

def overall(package, month=None, start_month=None, end_month=None, monthly=False, pkg_platform=None, data_source=None, pkg_version=None, pkg_python=None):

    # so we can pass in one or more packages
    # if more than one packages, e.g., ("pandas","dask") as a tuple or ["pandas","dask"] as a list, 
    # we need to them with "," so that in f-string it can read correctly as pkg_name in ("pandas","dask")
    if isinstance(package, tuple) or isinstance(package, list) :
        package= '","'.join(package)

    # if given year-month, read in data for this year-month for this package 
    if month is not None: 
        # if month is string, we change the type to datetime. 
        if isinstance(month, str):
            month = datetime.strptime(month, '%Y-%m')
        df = dd.read_parquet(f's3://anaconda-package-data/conda/monthly/{month.year}/{month.year}-{month.strftime("%m")}.parquet',
                         storage_options={'anon': True})
        df = df.query(f'pkg_name in ("{package}")')        
    
    # if given start_month and end_month, read in data between start_month and end_month
    elif start_month is not None and end_month is not None:
        #read in month between start_month and end_month
        file_list = []
        for month_i in pd.period_range(start_month, end_month, freq='M'):      
            file_list.append(f's3://anaconda-package-data/conda/monthly/{month_i.year}/{month_i}.parquet')
        df = dd.read_parquet(file_list,storage_options={'anon': True})
        df = df.query(f'pkg_name in ("{package}")')

    # if all optional arguments are None, read in all the data for a certain package
    else:
        # if all optional arguments are None, read in all the data for a certain package
        df = dd.read_parquet('s3://anaconda-package-data/conda/monthly/*/*.parquet',storage_options={'anon': True})
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
        monthly_counts = (df.groupby(['pkg_name','time']).counts.sum().compute())
        return monthly_counts[(monthly_counts!=0)].dropna()
    # return sum of all counts 
    else:
        total_counts = (df.groupby('pkg_name').counts.sum().compute()).dropna()  
        return  total_counts[(total_counts!=0)].dropna()


def _groupby(package, column, month, start_month, end_month, monthly):
    
    if isinstance(package, tuple) or isinstance(package, list)  :
        package= '","'.join(package)
    # if all optional arguments are None, read in all the data for a certain package    
    # df = dd.read_parquet(f's3://anaconda-package-data/conda/monthly/*/*.parquet',
    #                     columns=['time','pkg_name', column, 'counts'],
    #                     storage_options={'anon': True})
    # df = df.query(f'pkg_name in ("{package}")')

    # if given year-month, read in data for this year-month for this package 
    if month is not None: 
        if isinstance(month, str):
            month = datetime.strptime(month, '%Y-%m')
        df = dd.read_parquet(f's3://anaconda-package-data/conda/monthly/{month.year}/{month.year}-{month.strftime("%m")}.parquet',
                        columns=['time','pkg_name', column, 'counts'],
                        storage_options={'anon': True})

        print(type(df))
        print(len(df.index))
        print()

        df = df.query(f'pkg_name in ("{package}")')        

    # if given start_month and end_month, read in data between start_month and end_month
    elif start_month is not None and end_month is not None:
        #read in month between start_month and end_month
        file_list = []
        for month_i in pd.period_range(start_month, end_month, freq='M'):      
            file_list.append(f's3://anaconda-package-data/conda/monthly/{month_i.year}/{month_i}.parquet')
        df = dd.read_parquet(file_list,columns=['time','pkg_name', column, 'counts'], storage_options={'anon': True})
        df = df.query(f'pkg_name in ("{package}")') 

    # if all optional arguments are None, read in all the data for a certain package
    else:
        df = dd.read_parquet(f's3://anaconda-package-data/conda/monthly/*/*.parquet',
                        columns=['time','pkg_name', column, 'counts'],
                        storage_options={'anon': True})
        df = df.query(f'pkg_name in ("{package}")')

    print(df.compute())
    print(type(df))
    print(len(df.index))
    print(df)
    print()

    temp = df.compute()
    print(type(temp))
    print(len(temp.index))
    print(temp)
    print()

    # test = df.set_index(column, sorted=False)
    # print(type(test))
    # print(len(test.index))
    # print(test)
    # print()

    agg = temp.groupby(['pkg_name', 'time', column]).counts.sum()

    print(len(agg.index))
    exit()
    # group = df.groupby(['pkg_name',column])
    # print(df.groupby(['pkg_name',column]).counts.sum().compute())

    # if monthly, return monthly counts
    if monthly:
        agg = df.groupby(['pkg_name', 'time', column]).counts.sum().compute()
    # return sum of all counts 
    else:
        agg = df.groupby(['pkg_name',column]).counts.sum().compute()
    
    return agg[(agg!=0)].dropna()


def pkg_platform(package, month=None, start_month=None, end_month=None, monthly=False):
    return _groupby(package, 'pkg_platform', month, start_month, end_month, monthly)


def data_source(package, month=None, start_month=None, end_month=None, monthly=False):
    return _groupby(package, 'data_source', month, start_month, end_month, monthly)


def pkg_version(package, month=None, start_month=None, end_month=None, monthly=False):
    return _groupby(package, 'pkg_version', month, start_month, end_month, monthly)


def pkg_python(package, month=None, start_month=None, end_month=None, monthly=False):
    return _groupby(package, 'pkg_python', month, start_month, end_month, monthly)


def main():
    """Console script for condastats."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparserdest')

    parser_overall = subparsers.add_parser('overall')

    parser_overall.add_argument("package",
                        help="package name(s)",
                        nargs='+'
                       )

    parser_overall.add_argument("--month",
                        help="month - YYYY-MM (defalt: None)",
                        type=lambda d: datetime.strptime(d, '%Y-%m'),
                        default=None
                       )

    parser_overall.add_argument("--start_month",
                        help="start month - YYYY-MM (defalt: None)",
                        type=lambda d: datetime.strptime(d, '%Y-%m'),
                        default=None
                       )
 
    parser_overall.add_argument("--end_month",
                        help="end month - YYYY-MM (defalt: None)",
                        type=lambda d: datetime.strptime(d, '%Y-%m'),
                        default=None
                       )

    parser_overall.add_argument("--monthly",
                        help="return monthly values (defalt: False)",
                        action='store_true'
                       )

    parser_overall.add_argument("--pkg_platform",
                        help="package platform e.g., win-64, linux-32, osx-64. (defalt: None)",
                        default=None 
                       )
    
    parser_overall.add_argument("--pkg_python",
                        help="Python version e.g., 3.7 (defalt: None)",
                        default=None 
                       )
     
    parser_overall.add_argument("--pkg_version",
                        help="Python version e.g., 0.1.0 (defalt: None)",
                        default=None 
                       )   
    parser_overall.add_argument("--data_source",
                        help="Data source e.g., anaconda, conda-forge (defalt: None)",
                        default=None 
                       )  

    parser_platform = subparsers.add_parser('pkg_platform')

    parser_platform.add_argument("package",
                        help="package name(s)",
                        nargs='+'
                       )

    parser_platform.add_argument("--month",
                        help="month - YYYY-MM (defalt: None)",
                        type=lambda d: datetime.strptime(d, '%Y-%m'),
                        default=None
                       )

    parser_platform.add_argument("--start_month",
                        help="start month - YYYY-MM (defalt: None)",
                        type=lambda d: datetime.strptime(d, '%Y-%m'),
                        default=None
                       )
 
    parser_platform.add_argument("--end_month",
                        help="end month - YYYY-MM (defalt: None)",
                        type=lambda d: datetime.strptime(d, '%Y-%m'),
                        default=None
                       )

    parser_platform.add_argument("--monthly",
                        help="return monthly values (defalt: False)",
                        action='store_true'
                       )

    parser_source = subparsers.add_parser('data_source')

    parser_source.add_argument("package",
                        help="package name(s)",
                        nargs='+'
                       )

    parser_source.add_argument("--month",
                        help="month - YYYY-MM (defalt: None)",
                        type=lambda d: datetime.strptime(d, '%Y-%m'),
                        default=None
                       )
    parser_source.add_argument("--start_month",
                        help="start month - YYYY-MM (defalt: None)",
                        type=lambda d: datetime.strptime(d, '%Y-%m'),
                        default=None
                       )
 
    parser_source.add_argument("--end_month",
                        help="end month - YYYY-MM (defalt: None)",
                        type=lambda d: datetime.strptime(d, '%Y-%m'),
                        default=None
                       )

    parser_source.add_argument("--monthly",
                        help="return monthly values (defalt: False)",
                        action='store_true'
                       )


    parser_package_version = subparsers.add_parser('pkg_version')

    parser_package_version.add_argument("package",
                        help="package name(s)",
                        nargs='+'
                       )

    parser_package_version.add_argument("--month",
                        help="month - YYYY-MM (defalt: None)",
                        type=lambda d: datetime.strptime(d, '%Y-%m'),
                        default=None
                       )
    parser_package_version.add_argument("--start_month",
                        help="start month - YYYY-MM (defalt: None)",
                        type=lambda d: datetime.strptime(d, '%Y-%m'),
                        default=None
                       )
 
    parser_package_version.add_argument("--end_month",
                        help="end month - YYYY-MM (defalt: None)",
                        type=lambda d: datetime.strptime(d, '%Y-%m'),
                        default=None
                       )

    parser_package_version.add_argument("--monthly",
                        help="return monthly values (defalt: False)",
                        action='store_true'
                       )

    parser_python_version = subparsers.add_parser('pkg_python')

    parser_python_version.add_argument("package",
                        help="package name(s)",
                        nargs='+'
                       )

    parser_python_version.add_argument("--month",
                        help="month - YYYY-MM (defalt: None)",
                        type=lambda d: datetime.strptime(d, '%Y-%m'),
                        default=None
                       )
    parser_python_version.add_argument("--start_month",
                        help="start month - YYYY-MM (defalt: None)",
                        type=lambda d: datetime.strptime(d, '%Y-%m'),
                        default=None
                       )
 
    parser_python_version.add_argument("--end_month",
                        help="end month - YYYY-MM (defalt: None)",
                        type=lambda d: datetime.strptime(d, '%Y-%m'),
                        default=None
                       )

    parser_python_version.add_argument("--monthly",
                        help="return monthly values (defalt: False)",
                        action='store_true'
                       )

    args = parser.parse_args()

    if args.subparserdest == 'overall':
        print(overall(
            package=args.package,
            month=args.month, 
            start_month=args.start_month,
            end_month = args.end_month,
            monthly=args.monthly,
            pkg_platform=args.pkg_platform,
            data_source=args.data_source,
            pkg_version=args.pkg_version,
            pkg_python=args.pkg_python
            ))
    elif args.subparserdest == 'pkg_platform':
        print(pkg_platform(
            package=args.package, month=args.month, start_month=args.start_month, end_month=args.end_month,monthly=args.monthly
            ))
    elif args.subparserdest == 'data_source':
        print(data_source(
            package=args.package, month=args.month, start_month=args.start_month, end_month=args.end_month,monthly=args.monthly
            ))
    elif args.subparserdest == 'pkg_version':
        print(pkg_version(
            package=args.package, month=args.month, start_month=args.start_month, end_month=args.end_month,monthly=args.monthly
            ))
    elif args.subparserdest == 'pkg_python':
        print(pkg_python(
            package=args.package, month=args.month, start_month=args.start_month, end_month=args.end_month,monthly=args.monthly
            ))


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
