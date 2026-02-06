"""Tests for the pure-pandas query functions in condastats._query.

These tests use synthetic DataFrames and never touch S3, so they run fast
and without network access.
"""

import pandas as pd
import pytest

from condastats._query import query_grouped, query_overall, top_packages

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def sample_df():
    """A small DataFrame mimicking the real Anaconda package-data schema."""
    return pd.DataFrame(
        {
            "pkg_name": [
                "pandas",
                "pandas",
                "pandas",
                "numpy",
                "numpy",
                "numpy",
                "scipy",
                "scipy",
            ],
            "counts": [100, 200, 50, 300, 150, 250, 80, 120],
            "time": [
                "2024-01",
                "2024-01",
                "2024-02",
                "2024-01",
                "2024-01",
                "2024-02",
                "2024-01",
                "2024-02",
            ],
            "pkg_platform": [
                "linux-64",
                "osx-64",
                "linux-64",
                "linux-64",
                "win-64",
                "linux-64",
                "linux-64",
                "osx-64",
            ],
            "data_source": [
                "anaconda",
                "conda-forge",
                "anaconda",
                "anaconda",
                "anaconda",
                "conda-forge",
                "conda-forge",
                "anaconda",
            ],
            "pkg_version": [
                "2.0.0",
                "2.0.0",
                "2.1.0",
                "1.25.0",
                "1.25.0",
                "1.26.0",
                "1.11.0",
                "1.12.0",
            ],
            "pkg_python": [
                "3.10",
                "3.11",
                "3.10",
                "3.10",
                "3.11",
                "3.10",
                "3.10",
                "3.11",
            ],
        }
    )


# ---------------------------------------------------------------------------
# query_overall – basics
# ---------------------------------------------------------------------------


def test_overall_all_packages(sample_df):
    """No package filter returns every package."""
    result = query_overall(sample_df)
    assert set(result.index) == {"pandas", "numpy", "scipy"}


@pytest.mark.parametrize(
    "package",
    [
        "pandas",
        ["pandas"],
        ("pandas",),
    ],
    ids=["str", "list", "tuple"],
)
def test_overall_single_package_input_types(sample_df, package):
    """String, list, and tuple all resolve to the same result."""
    result = query_overall(sample_df, package=package)
    assert result.loc["pandas"] == 350


def test_overall_multiple_packages(sample_df):
    result = query_overall(sample_df, package=["pandas", "numpy"])
    assert "pandas" in result.index
    assert "numpy" in result.index
    assert "scipy" not in result.index


@pytest.mark.parametrize(
    "package,expected_total",
    [
        ("pandas", 350),
        ("numpy", 700),
        ("scipy", 200),
    ],
)
def test_overall_totals(sample_df, package, expected_total):
    result = query_overall(sample_df, package=package)
    assert result.loc[package] == expected_total


# ---------------------------------------------------------------------------
# query_overall – monthly / complete
# ---------------------------------------------------------------------------


def test_overall_monthly(sample_df):
    result = query_overall(sample_df, package="pandas", monthly=True)
    assert result.index.nlevels == 2
    assert ("pandas", "2024-01") in result.index
    assert ("pandas", "2024-02") in result.index


def test_overall_complete(sample_df):
    result = query_overall(sample_df, package="pandas", complete=True)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3


# ---------------------------------------------------------------------------
# query_overall – filters
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "filters,expected",
    [
        ({"pkg_platform": "linux-64"}, 150),
        ({"data_source": "conda-forge"}, 200),
        ({"pkg_version": "2.0.0"}, 300),
        ({"pkg_python": "3.11"}, 200),
        ({"pkg_platform": "linux-64", "data_source": "anaconda"}, 150),
    ],
    ids=["platform", "source", "version", "python", "combined"],
)
def test_overall_filters(sample_df, filters, expected):
    result = query_overall(sample_df, package="pandas", **filters)
    assert result.loc["pandas"] == expected


# ---------------------------------------------------------------------------
# query_grouped
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "column,package,expected_keys",
    [
        ("pkg_platform", "pandas", [("pandas", "linux-64"), ("pandas", "osx-64")]),
        ("data_source", "numpy", [("numpy", "anaconda"), ("numpy", "conda-forge")]),
        ("pkg_python", "pandas", [("pandas", "3.10"), ("pandas", "3.11")]),
    ],
    ids=["platform", "source", "python"],
)
def test_grouped_single_package(sample_df, column, package, expected_keys):
    result = query_grouped(sample_df, column, package=package)
    assert result.index.nlevels == 2
    for key in expected_keys:
        assert key in result.index


@pytest.mark.parametrize(
    "column",
    ["pkg_platform", "data_source", "pkg_version", "pkg_python"],
)
def test_grouped_multiple_packages(sample_df, column):
    result = query_grouped(sample_df, column, package=["pandas", "numpy"])
    pkgs = result.index.get_level_values("pkg_name").unique()
    assert "pandas" in pkgs
    assert "numpy" in pkgs


@pytest.mark.parametrize(
    "column",
    ["pkg_platform", "data_source"],
)
def test_grouped_monthly(sample_df, column):
    result = query_grouped(sample_df, column, package="pandas", monthly=True)
    assert result.index.nlevels == 3


def test_grouped_no_package_filter(sample_df):
    result = query_grouped(sample_df, "data_source")
    pkgs = result.index.get_level_values("pkg_name").unique()
    assert len(pkgs) == 3


def test_grouped_version_count(sample_df):
    result = query_grouped(sample_df, "pkg_version", package="numpy")
    assert len(result) == 2  # 1.25.0 and 1.26.0


# ---------------------------------------------------------------------------
# top_packages
# ---------------------------------------------------------------------------


def test_top_packages_order_and_totals(sample_df):
    result = top_packages(sample_df, n=3)
    assert list(result.index) == ["numpy", "pandas", "scipy"]
    assert result.loc["numpy"] == 700
    assert result.loc["pandas"] == 350
    assert result.loc["scipy"] == 200


@pytest.mark.parametrize("n", [1, 2, 3])
def test_top_packages_n(sample_df, n):
    result = top_packages(sample_df, n=n)
    assert len(result) == n


def test_top_packages_descending(sample_df):
    result = top_packages(sample_df)
    values = result.values.tolist()
    assert values == sorted(values, reverse=True)
