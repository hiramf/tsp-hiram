Running log of the steps/process and everything which went on to solve this problem.

Log
------------
- Day 1: 4/29/2020

  + Was already familiar with using genetic algorithms to solve a TSP-type problem.
  + Read the Wiki about the TSP to more fully understand it.
  + Decided to first use a cookiecutter template as my starting point.


- Day 2: 4/30/2020

  + Setup my environment with cookiecutter and create a github repo
  + Made sure the repo and third-party services were all working (Travis, CodeCov, ReadTheDocs)
  + Removed tests from Tox for python versions I'm not going to worry about at the moment
  + Not going to worry about setting everything up perfectly.
  + Primary objective for today was getting Pytest/Tox to run some basic tests successfully.
  + Also getting VS Code setup the way I like it (i.e. F5 for running the tests).
  + Started with two basic functions:

    1. creating a distance matrix
    2. returning a tour from a distance matrix

  + Created tests for those two functions