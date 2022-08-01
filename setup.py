# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import versioneer

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [ 
    'numpy>=1.16.5',
    'dask[dataframe]',
    'pyarrow',
    's3fs'
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
