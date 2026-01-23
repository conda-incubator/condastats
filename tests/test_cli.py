"""Tests for the CLI main() function.

Minimal tests to cover argument parsing - logic is tested in test_overall.py
and test_groupby.py.
"""
import sys

import pytest

from condastats.cli import main


def test_main_overall(monkeypatch, capsys):
    """Test main() parses overall subcommand correctly."""
    monkeypatch.setattr(sys, 'argv', [
        'condastats', 'overall', 'pandas', '--month', '2019-01'
    ])
    main()
    captured = capsys.readouterr()
    assert '932443' in captured.out


def test_main_overall_with_options(monkeypatch, capsys):
    """Test main() parses all overall options."""
    monkeypatch.setattr(sys, 'argv', [
        'condastats', 'overall', 'pandas',
        '--month', '2019-01',
        '--pkg_platform', 'linux-32',
        '--data_source', 'anaconda',
        '--pkg_version', '0.10.0',
        '--pkg_python', '2.6',
        '--complete'
    ])
    main()
    captured = capsys.readouterr()
    assert 'pandas' in captured.out


def test_main_overall_date_range(monkeypatch, capsys):
    """Test main() parses date range options."""
    monkeypatch.setattr(sys, 'argv', [
        'condastats', 'overall', 'pandas',
        '--start_month', '2019-01',
        '--end_month', '2019-02',
        '--monthly'
    ])
    main()
    captured = capsys.readouterr()
    assert 'pandas' in captured.out


@pytest.mark.parametrize("subcommand", [
    'pkg_platform', 'data_source', 'pkg_version', 'pkg_python'
])
def test_main_groupby_subcommands(monkeypatch, capsys, subcommand):
    """Test main() parses groupby subcommands."""
    monkeypatch.setattr(sys, 'argv', [
        'condastats', subcommand, 'pandas', '--month', '2019-01'
    ])
    main()
    captured = capsys.readouterr()
    assert 'pandas' in captured.out
