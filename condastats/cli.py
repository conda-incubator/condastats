"""Command-line interface for condastats."""

import argparse
import sys
from datetime import datetime

from condastats import __version__
from condastats._core import (
    data_source,
    overall,
    pkg_platform,
    pkg_python,
    pkg_version,
)


def _month_type(value: str) -> datetime:
    """Parse a YYYY-MM string into a datetime."""
    try:
        return datetime.strptime(value, "%Y-%m")
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"invalid month format: '{value}' (expected YYYY-MM)"
        )


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    """Add arguments shared by all subcommands."""
    parser.add_argument("package", help="package name(s)", nargs="+")
    parser.add_argument(
        "--month",
        help="month - YYYY-MM (default: None)",
        type=_month_type,
        default=None,
    )
    parser.add_argument(
        "--start_month",
        help="start month - YYYY-MM (default: None)",
        type=_month_type,
        default=None,
    )
    parser.add_argument(
        "--end_month",
        help="end month - YYYY-MM (default: None)",
        type=_month_type,
        default=None,
    )
    parser.add_argument(
        "--monthly",
        help="return monthly values (default: False)",
        action="store_true",
    )


def _build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="condastats",
        description="Query download statistics for conda packages.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command")

    # overall subcommand
    parser_overall = subparsers.add_parser(
        "overall", help="Get overall download counts"
    )
    _add_common_args(parser_overall)
    parser_overall.add_argument(
        "--complete",
        help="return all values (default: False)",
        action="store_true",
    )
    parser_overall.add_argument(
        "--pkg_platform",
        help="package platform, e.g. win-64, linux-32, osx-64 (default: None)",
        default=None,
    )
    parser_overall.add_argument(
        "--pkg_python",
        help="Python version, e.g. 3.7 (default: None)",
        default=None,
    )
    parser_overall.add_argument(
        "--pkg_version",
        help="package version, e.g. 0.1.0 (default: None)",
        default=None,
    )
    parser_overall.add_argument(
        "--data_source",
        help="data source, e.g. anaconda, conda-forge (default: None)",
        default=None,
    )

    # groupby subcommands
    for name, help_text in [
        ("pkg_platform", "Get downloads grouped by platform"),
        ("data_source", "Get downloads grouped by data source"),
        ("pkg_version", "Get downloads grouped by package version"),
        ("pkg_python", "Get downloads grouped by Python version"),
    ]:
        sub = subparsers.add_parser(name, help=help_text)
        _add_common_args(sub)

    return parser


def _validate_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    """Validate argument combinations."""
    if args.command is None:
        parser.print_help()
        raise SystemExit(2)

    has_start = args.start_month is not None
    has_end = args.end_month is not None
    if has_start != has_end:
        parser.error("--start_month and --end_month must be used together")

    if args.month is not None and (has_start or has_end):
        parser.error("--month cannot be used with --start_month/--end_month")


_GROUPBY_FUNCS = {
    "pkg_platform": pkg_platform,
    "data_source": data_source,
    "pkg_version": pkg_version,
    "pkg_python": pkg_python,
}


def main(argv: list[str] | None = None) -> int:
    """Entry point for the condastats CLI.

    Parameters
    ----------
    argv : list of str, optional
        Command-line arguments. Defaults to ``sys.argv[1:]``.

    Returns
    -------
    int
        Exit code (0 for success).
    """
    import pandas as pd

    pd.set_option("display.max_rows", None)

    parser = _build_parser()
    args = parser.parse_args(argv)
    _validate_args(args, parser)

    common_kwargs = dict(
        package=args.package,
        month=args.month,
        start_month=args.start_month,
        end_month=args.end_month,
        monthly=args.monthly,
    )

    if args.command == "overall":
        result = overall(
            **common_kwargs,
            complete=args.complete,
            pkg_platform=args.pkg_platform,
            data_source=args.data_source,
            pkg_version=args.pkg_version,
            pkg_python=args.pkg_python,
        )
    else:
        func = _GROUPBY_FUNCS[args.command]
        result = func(**common_kwargs)

    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
