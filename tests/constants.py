"""Test constants and expected values."""

TEST_MONTH = "2019-01"
TEST_START_MONTH = "2019-01"
TEST_END_MONTH = "2019-02"

# Test packages with known download counts for 2019-01
TEST_PACKAGES_DATA = {
    "pandas": {"overall": 932443, "platform": "linux-64", "source": "anaconda"},
    "numpy": {"overall": 2301341, "platform": "linux-64", "source": "anaconda"},
    "scipy": {"overall": 1065864, "platform": "linux-64", "source": "anaconda"},
    "requests": {"overall": 889856, "platform": "linux-64", "source": "anaconda"},
    "dask": {"overall": 221200, "platform": "linux-64", "source": "anaconda"},
}
