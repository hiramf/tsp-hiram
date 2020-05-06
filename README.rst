========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - |commits-since|
.. |docs| image:: https://readthedocs.org/projects/tsp-hiram/badge/?style=flat
    :target: https://readthedocs.org/projects/tsp-hiram
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/hiramf/tsp-hiram.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/hiramf/tsp-hiram

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/hiramf/tsp-hiram?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/hiramf/tsp-hiram

.. |requires| image:: https://requires.io/github/hiramf/tsp-hiram/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/hiramf/tsp-hiram/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/hiramf/tsp-hiram/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/hiramf/tsp-hiram

.. |commits-since| image:: https://img.shields.io/github/commits-since/hiramf/tsp-hiram/v0.2.1.svg
    :alt: Commits since latest release
    :target: https://github.com/hiramf/tsp-hiram/compare/v0.2.1...master



.. end-badges

Hiram Foster's solution to the Traveling Salesman coding challenge.

There were two problems to solve:

#. Given an input of list of co-ordinates find the path which is the shortest distance which touches ALL these points
#. Given an input of list of co-ordinates and fixed distance identify the maximum number of points which can be touched

Solution Artifacts required:

+ Working Code
+ Unit Test Cases (can be run with Tox/pytest)
+ Exception and Edge Cases: Documented in the log and accounted for the the code
+ Running `log <https://tsp-hiram.readthedocs.io/en/latest/log.html>`_ of the steps/process and everything which went on to solve this problem


Installation
============

You can install the in-development version with::

    pip install https://github.com/hiramf/tsp-hiram/archive/master.zip


Documentation
=============

This is a module than can be installed like any other normal Python package and imported into scripts, Jupyter, etc.

To use the CLI, run:

.. code-block:: python

   tsp-hiram filename.csv --max 100

Where ```filename.csv``` is a two column csv file of coordinates with a header and ```--max 100``` is an optional argument to set the maximum distance of the soution.



https://tsp-hiram.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
