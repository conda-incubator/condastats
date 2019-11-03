============
condastats
============


Examples
---------------

condastats overall
~~~~~~~~~~~~~~~~~~~~~~
pandas package download counts for Jan. 2019: 

:: 

   condastats overall pandas 2019-01
>>> 932443


pandas package download counts for Jan. 2019 for specific package platform, data source, package version, and python version: 

:: 

   condastats overall pandas 2019-01 --package_platform linux-32 --source anaconda --package_version 0.10.0 --python_version 2.6
>>> 12


condastats platform
~~~~~~~~~~~~~~~~~~~~~~
pandas package download counts for each operating system for Jan. 2019:

:: 

   condastats platform pandas 2019-01

+--------------+--------+
|              |        | 
+==============+========+
| linux-32     | 1303   | 
+--------------+--------+
| linux-64     | 71220  | 
+--------------+--------+
| linux-aarch64| 0      | 
+--------------+--------+
| linux-armv6l | 0      | 
+--------------+--------+
| linux-armv7l | 21     | 
+--------------+--------+
| linux-ppc64le| 1612   | 
+--------------+--------+
| osx-32       | 7      | 
+--------------+--------+
| osx-64       | 76963  | 
+--------------+--------+
| win-32       | 6435   | 
+--------------+--------+
| win-64       | 134882 | 
+--------------+--------+


condastats data source
~~~~~~~~~~~~~~~~~~~~~~
pandas package download counts for each data source for Jan. 2019:

:: 

   condastats source pandas 2019-01

+--------------+--------+
|              |        | 
+==============+========+
| anaconda     | 673503 | 
+--------------+--------+
| conda-forge  | 258940 | 
+--------------+--------+


condastats python_version
~~~~~~~~~~~~~~~~~~~~~~
pandas package download counts for each python version for Jan. 2019:

:: 

   condastats python_version pandas 2019-01

+--------------+--------+
|              |        | 
+==============+========+
| 2.6          | 1466   | 
+--------------+--------+
| 2.7          | 247949 | 
+--------------+--------+
| 3.3          | 1119   | 
+--------------+--------+
| 3.4          | 9251   | 
+--------------+--------+
| 3.5          | 104445 | 
+--------------+--------+
| 3.6          | 468838 | 
+--------------+--------+
| 3.7          | 99375  | 
+--------------+--------+


condastats package_version
~~~~~~~~~~~~~~~~~~~~~~
pandas package download counts for each package version for Jan. 2019:

:: 

   condastats package_version pandas 2019-01

+--------------+--------+
|              |        | 
+==============+========+
| 0.10.0       | 180    | 
+--------------+--------+
| 0.10.1       | 180    | 
+--------------+--------+
| 0.11.0       | 180    | 
+--------------+--------+
| 0.12.0       | 180    | 
+--------------+--------+
| 0.13.0       | 180    | 
+--------------+--------+
| 0.13.1       | 180    | 
+--------------+--------+
| 0.14.0       | 180    | 
+--------------+--------+
