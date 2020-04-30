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
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
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

.. |version| image:: https://img.shields.io/pypi/v/tsp-hiram.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/tsp-hiram

.. |wheel| image:: https://img.shields.io/pypi/wheel/tsp-hiram.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/tsp-hiram

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/tsp-hiram.svg
    :alt: Supported versions
    :target: https://pypi.org/project/tsp-hiram

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/tsp-hiram.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/tsp-hiram

.. |commits-since| image:: https://img.shields.io/github/commits-since/hiramf/tsp-hiram/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/hiramf/tsp-hiram/compare/v0.0.0...master



.. end-badges

Hiram Foster's solution to the Traveling Salesman coding challenge.

* Free software: MIT license

Installation
============

::

    pip install tsp-hiram

You can also install the in-development version with::

    pip install https://github.com/hiramf/tsp-hiram/archive/master.zip


Documentation
=============


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
