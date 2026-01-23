# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import versioneer

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'numpy>=1.16.5,<2.0.0',
    'pandas>=1.5.0,<2.0.0',  # pandas 2.x has incompatibility with legacy S3 parquet files
    'dask[dataframe]>=2023.1.0,<2024.3.0',  # dask 2024.3+ requires pandas 2.x
    'pyarrow>=10.0.0,<15.0.0',  # pyarrow 10-14 works with pandas 1.x and legacy parquet
    's3fs>=2023.1.0'  # Modern s3fs
]

import os
if not os.getenv('READTHEDOCS'):
    requirements.append('python-snappy')

setup_requirements = [ ]

test_requirements = [
    'pytest'
 ]

setup(
    author="Sophia Man Yang",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="Conda package stats CLI",
    entry_points={
        'console_scripts': [
            'condastats=condastats.cli:main',
        ],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme,
    include_package_data=True,
    keywords='condastats',
    name='condastats',
    packages=find_packages(include=['condastats']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/sophiamyang/condastats',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    zip_safe=False,
)
