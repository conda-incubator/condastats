from condastats.cli import overall, pkg_platform, pkg_version, pkg_python, data_source

def test_overall1():
    x = overall(['pandas','dask'], month='2019-01')
    assert x.loc['pandas'] == 932443
    assert x.loc['dask'] == 221200

def test_overall2():
    x = overall('pandas',month='2019-01', pkg_platform='linux-32',data_source='anaconda',pkg_version='0.10.0',pkg_python=2.6)
    assert x.loc['pandas'] == 12


