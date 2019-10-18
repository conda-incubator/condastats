# -*- coding: utf-8 -*-

"""Console script for condastats."""
import sys
import dask.dataframe as dd
from datetime import datetime
import intake
import numpy as np
import pandas as pd
import argparse
import warnings

cat = intake.open_catalog('https://raw.githubusercontent.com/ContinuumIO/anaconda-package-data/master/catalog/anaconda_package_data.yaml')

def load_pkg_month(year, month, package):
    df = cat.anaconda_package_data_by_month(year=year, 
                                            month=month, 
                                            columns=['pkg_name', 'counts']).to_dask()
    df = df.query(f'pkg_name in ("{package}")')
    warnings.simplefilter("ignore", UserWarning) #ignore UserWarning: Non-categorical multi-index is likely brittle warnings.warn("Non-categorical multi-index is likely brittle")
    print(df.counts.sum().compute())

def pkg_sys_month(year, month, package):
    df = cat.anaconda_package_data_by_month(year=year, 
                                            month=month, 
                                            columns=['pkg_name', 'pkg_platform', 'counts']).to_dask()
    df = df.query(f'pkg_name in ("{package}")')
    warnings.simplefilter("ignore", UserWarning) #ignore UserWarning: Non-categorical multi-index is likely brittle warnings.warn("Non-categorical multi-index is likely brittle")
    print(df.groupby('pkg_platform').counts.sum().compute())


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
    
    parser_system = subparsers.add_parser('system')

    parser_system.add_argument("package",
                        help="package name"
                       )

    parser_system.add_argument("month",
                        help="month - YYYY-MM",
                        type=lambda d: datetime.strptime(d, '%Y-%m')
                       )
    args = parser.parse_args()

    if args.subparserdest == 'overall':
        load_pkg_month(args.month.year, args.month.month, args.package)
    elif args.subparserdest == 'system':
        pkg_sys_month(args.month.year, args.month.month, args.package)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
