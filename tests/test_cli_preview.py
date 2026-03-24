"""Tests for CLI routing, deprecation messaging, and preview mode."""

from unittest.mock import patch

import pandas as pd
import pytest

from condastats.cli import main
from condastats.cli_flags import _build_parser as _build_preview_parser
from condastats.cli_flags import _validate_args as _validate_preview_args

_FAKE_SERIES = pd.Series(
    [932443], index=pd.Index(["pandas"], name="pkg_name"), name="counts"
)
_FAKE_DF = pd.DataFrame(
    {"pkg_name": ["pandas"], "counts": [932443], "time": ["2019-01"]}
)
_FAKE_GROUPBY = pd.Series(
    [500000, 432443],
    index=pd.MultiIndex.from_tuples(
        [("pandas", "linux-64"), ("pandas", "osx-64")],
        names=["pkg_name", "pkg_platform"],
    ),
    name="counts",
)


class TestRouter:
    """Tests for top-level router dispatch."""

    @patch("condastats.cli.cli_legacy.main", return_value=0)
    def test_routes_legacy_mode_without_preview(self, mock_legacy):
        """main() should route raw args to legacy mode by default."""
        result = main(["overall", "pandas", "--month", "2019-01"])
        assert result == 0
        mock_legacy.assert_called_once_with(["overall", "pandas", "--month", "2019-01"])

    @patch("condastats.cli.cli_flags.main", return_value=7)
    def test_routes_preview_mode_when_flag_present(self, mock_preview):
        """main() should route preview flag invocations to the preview module."""
        result = main(["--preview", "pandas", "--month", "2019-01"])
        assert result == 7
        mock_preview.assert_called_once_with(["pandas", "--month", "2019-01"])

    @patch("condastats.cli.cli_flags.main", return_value=2)
    def test_routes_preview_mode_and_strips_all_preview_flags(self, mock_preview):
        """Router should remove preview routing flags before delegation."""
        main(["--preview", "pandas", "--preview", "--month", "2019-01"])
        mock_preview.assert_called_once_with(["pandas", "--month", "2019-01"])

    @patch("condastats.cli.cli_flags.main", return_value=9)
    def test_router_preserves_exit_code(self, mock_preview):
        """Router should return the delegated exit code."""
        assert main(["--preview", "pandas"]) == 9

    @patch("condastats.cli.cli_legacy.main", return_value=0)
    def test_preview_flag_after_subcommand_does_not_switch_modes(self, mock_legacy):
        """Only the global preview flag should trigger preview routing."""
        result = main(["overall", "pandas", "--", "--preview"])
        assert result == 0
        mock_legacy.assert_called_once_with(["overall", "pandas", "--", "--preview"])


class TestLegacyDeprecation:
    """Tests for legacy deprecation messaging."""

    @patch("condastats.cli_legacy.overall", return_value=_FAKE_SERIES)
    def test_legacy_mode_emits_deprecation_warning(self, mock_overall, capsys):
        """Legacy commands should emit a deprecation warning."""
        result = main(["overall", "pandas", "--month", "2019-01"])
        assert result == 0
        captured = capsys.readouterr()
        assert "Deprecation warning" in captured.err
        assert "condastats --preview pandas --month 2024-01" in captured.err
        mock_overall.assert_called_once()

    @patch("condastats.cli_legacy._emit_deprecation_warning")
    def test_no_warning_on_parser_failure(self, mock_warning):
        """Parser failures should not emit a deprecation warning."""
        with pytest.raises(SystemExit):
            main(["overall", "pandas", "--month", "not-a-date"])
        mock_warning.assert_not_called()


class TestPreviewParser:
    """Tests for preview parser setup and validation."""

    def test_preview_overall_parses(self):
        """Preview overall queries should parse without a group."""
        parser = _build_preview_parser()
        args = parser.parse_args(["pandas", "--month", "2019-01"])
        assert args.group is None
        assert args.package == ["pandas"]

    def test_preview_group_parses(self):
        """Preview group queries should parse with a single group value."""
        parser = _build_preview_parser()
        args = parser.parse_args(
            ["--group", "pkg_platform", "pandas", "--month", "2019-01"]
        )
        assert args.group == "pkg_platform"
        assert args.package == ["pandas"]

    def test_preview_group_with_overall_filters_errors(self):
        """Grouped preview queries should reject overall-only filter flags."""
        parser = _build_preview_parser()
        args = parser.parse_args(
            [
                "--group",
                "pkg_platform",
                "pandas",
                "--month",
                "2019-01",
                "--pkg_platform",
                "linux-64",
            ]
        )
        with pytest.raises(SystemExit):
            _validate_preview_args(args, parser)


class TestPreviewMainIntegration:
    """Integration tests for preview CLI dispatch."""

    @patch("condastats.cli_flags.overall", return_value=_FAKE_DF)
    def test_preview_main_overall(self, mock_overall, capsys):
        """Preview overall mode should call overall() and print results."""
        result = main(["--preview", "pandas", "--month", "2019-01"])
        assert result == 0
        captured = capsys.readouterr()
        assert "pandas" in captured.out
        assert captured.err == ""
        call_kwargs = mock_overall.call_args.kwargs
        assert call_kwargs["package"] == ["pandas"]

    @patch("condastats.cli_flags.overall", return_value=_FAKE_DF)
    def test_preview_main_overall_with_filters(self, mock_overall, capsys):
        """Preview overall mode should pass supported filters to overall()."""
        result = main(
            [
                "--preview",
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
        assert result == 0
        captured = capsys.readouterr()
        assert "pandas" in captured.out
        call_kwargs = mock_overall.call_args.kwargs
        assert call_kwargs["pkg_platform"] == "linux-32"
        assert call_kwargs["data_source"] == "anaconda"
        assert call_kwargs["pkg_version"] == "0.10.0"
        assert call_kwargs["pkg_python"] == "2.6"
        assert call_kwargs["complete"] is True

    @patch(
        "condastats.cli_flags._GROUPBY_FUNCS",
        {"pkg_platform": lambda **kwargs: _FAKE_GROUPBY},
    )
    def test_preview_main_groupby(self, capsys):
        """Preview group mode should dispatch to the correct function."""
        result = main(
            ["--preview", "--group", "pkg_platform", "pandas", "--month", "2019-01"]
        )
        assert result == 0
        captured = capsys.readouterr()
        assert "pandas" in captured.out
