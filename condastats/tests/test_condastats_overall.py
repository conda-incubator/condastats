from condastats.cli import load_pkg_month, pkg_platform_month, pkg_python_month, pkg_version_month, data_source_month

def test_load_pkg_month1():
    x = load_pkg_month('pandas', month='2019-01')
    assert x == 932443

def test_load_pkg_month2():
    x = load_pkg_month('pandas',month='2019-01', pkg_platform='linux-32',data_source='anaconda',pkg_version='0.10.0',pkg_python=2.6)
    assert x == 12


