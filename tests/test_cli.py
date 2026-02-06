"""Tests for the CLI argument parsing and entry point.

Tests for the underlying data functions are in test_overall.py and test_groupby.py.
The CLI integration tests here mock the data layer to avoid S3 calls and focus on
verifying that main() wires argument parsing to the correct functions.
"""

from unittest.mock import patch

import pandas as pd
import pytest

from condastats import __version__
from condastats.cli import _build_parser, _validate_args, main

# Fake data returned by mocked functions
_FAKE_SERIES = pd.Series(
    [932443], index=pd.Index(["pandas"], name="pkg_name"), name="counts"
)
_FAKE_DF = pd.DataFrame(
    {"pkg_name": ["pandas"], "counts": [932443], "time": ["2019-01"]}
)
_FAKE_MONTHLY = pd.Series(
    [932443, 1049595],
    index=pd.MultiIndex.from_tuples(
        [("pandas", "2019-01"), ("pandas", "2019-02")],
        names=["pkg_name", "time"],
    ),
    name="counts",
)
_FAKE_GROUPBY = pd.Series(
    [500000, 432443],
    index=pd.MultiIndex.from_tuples(
        [("pandas", "linux-64"), ("pandas", "osx-64")],
        names=["pkg_name", "pkg_platform"],
    ),
    name="counts",
)


class TestParserConstruction:
    """Tests for argument parser setup."""

    def test_version_flag(self, capsys):
        """--version should print version and exit."""
        parser = _build_parser()
        with pytest.raises(SystemExit, match="0"):
            parser.parse_args(["--version"])
        captured = capsys.readouterr()
        assert __version__ in captured.out

    def test_no_subcommand_exits(self):
        """Running without a subcommand should exit with code 2."""
        with pytest.raises(SystemExit, match="2"):
            main([])

    def test_overall_subcommand_parses(self):
        """overall subcommand should parse correctly."""
        parser = _build_parser()
        args = parser.parse_args(["overall", "pandas", "--month", "2019-01"])
        assert args.command == "overall"
        assert args.package == ["pandas"]

    def test_groupby_subcommand_parses(self):
        """groupby subcommands should parse correctly."""
        parser = _build_parser()
        for cmd in ("pkg_platform", "data_source", "pkg_version", "pkg_python"):
            args = parser.parse_args([cmd, "numpy", "--month", "2019-01"])
            assert args.command == cmd
            assert args.package == ["numpy"]

    def test_multiple_packages(self):
        """Multiple package names should be parsed as a list."""
        parser = _build_parser()
        args = parser.parse_args(["overall", "pandas", "numpy", "scipy"])
        assert args.package == ["pandas", "numpy", "scipy"]

    def test_month_format_invalid(self):
        """Invalid month format should raise an error."""
        parser = _build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["overall", "pandas", "--month", "not-a-date"])


class TestArgValidation:
    """Tests for argument validation logic."""

    def test_start_without_end(self):
        """--start_month without --end_month should error."""
        parser = _build_parser()
        args = parser.parse_args(["overall", "pandas", "--start_month", "2019-01"])
        with pytest.raises(SystemExit):
            _validate_args(args, parser)

    def test_end_without_start(self):
        """--end_month without --start_month should error."""
        parser = _build_parser()
        args = parser.parse_args(["overall", "pandas", "--end_month", "2019-02"])
        with pytest.raises(SystemExit):
            _validate_args(args, parser)

    def test_month_with_range(self):
        """--month with --start_month/--end_month should error."""
        parser = _build_parser()
        args = parser.parse_args(
            [
                "overall",
                "pandas",
                "--month",
                "2019-01",
                "--start_month",
                "2019-01",
                "--end_month",
                "2019-02",
            ]
        )
        with pytest.raises(SystemExit):
            _validate_args(args, parser)


class TestMainIntegration:
    """Integration tests that call main() with mocked data functions.

    These verify that main() correctly wires CLI arguments to the underlying
    functions. Actual data correctness is tested in test_overall.py and
    test_groupby.py.
    """

    @patch("condastats.cli.overall", return_value=_FAKE_SERIES)
    def test_main_overall(self, mock_overall, capsys):
        """main() should call overall() and print results."""
        result = main(["overall", "pandas", "--month", "2019-01"])
        assert result == 0
        captured = capsys.readouterr()
        assert "932443" in captured.out
        mock_overall.assert_called_once()
        call_kwargs = mock_overall.call_args
        assert call_kwargs.kwargs["package"] == ["pandas"]

    @patch("condastats.cli.overall", return_value=_FAKE_DF)
    def test_main_overall_with_filters(self, mock_overall, capsys):
        """main() should pass all filter options to overall()."""
        main(
            [
                "overall",
                "pandas",
                "--month",
                "2019-01",
                "--pkg_platform",
                "linux-32",
                "--data_source",
                "anaconda",
                "--pkg_version",
                "0.10.0",
                "--pkg_python",
                "2.6",
                "--complete",
            ]
        )
        captured = capsys.readouterr()
        assert "pandas" in captured.out
        call_kwargs = mock_overall.call_args.kwargs
        assert call_kwargs["pkg_platform"] == "linux-32"
        assert call_kwargs["data_source"] == "anaconda"
        assert call_kwargs["pkg_version"] == "0.10.0"
        assert call_kwargs["pkg_python"] == "2.6"
        assert call_kwargs["complete"] is True

    @patch("condastats.cli.overall", return_value=_FAKE_MONTHLY)
    def test_main_overall_date_range(self, mock_overall, capsys):
        """main() should pass date range options to overall()."""
        main(
            [
                "overall",
                "pandas",
                "--start_month",
                "2019-01",
                "--end_month",
                "2019-02",
                "--monthly",
            ]
        )
        captured = capsys.readouterr()
        assert "pandas" in captured.out
        call_kwargs = mock_overall.call_args.kwargs
        assert call_kwargs["monthly"] is True
        assert call_kwargs["start_month"] is not None
        assert call_kwargs["end_month"] is not None

    @pytest.mark.parametrize(
        "subcommand",
        [
            "pkg_platform",
            "data_source",
            "pkg_version",
            "pkg_python",
        ],
    )
    def test_main_groupby_subcommands(self, capsys, subcommand):
        """main() should dispatch to the correct groupby function."""
        mock_fn = lambda **kwargs: _FAKE_GROUPBY  # noqa: E731
        with patch.dict("condastats.cli._GROUPBY_FUNCS", {subcommand: mock_fn}):
            main([subcommand, "pandas", "--month", "2019-01"])
            captured = capsys.readouterr()
            assert "pandas" in captured.out
