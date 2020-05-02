Running log of the steps/process and everything which went on to solve this problem.

Log
------------

Day 1: 4/29/2020
################

+ Was already familiar with using genetic algorithms to solve a TSP-type problem.
+ Read the Wiki about the TSP to more fully understand it.
+ Decided to first use a cookiecutter template as my starting point.

Day 2: 4/30/2020
################

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

Day 3: 5/1/2020
################

+ Goal is to implement a solution

  1. Create coordinates to use for tests
  2. Choose an algorithm to use for my soution. Algorithm must allow setting a maximum distance for the 2nd requirement.

+ Decided to use the `python-mip library <https://python-mip.readthedocs.io/en/latest/examples.html>`_

  + Doesn't require coding my own solution
  + Branch and Cut is the current record holder for the TSP, `solving a problem with 85,900 cities <https://en.wikipedia.org/wiki/Travelling_salesman_problem#Computing_a_solution/>`_.
  + Allows defining a custom objective function, which will satisfy both problems
  + Implemented preliminary solution working and corresponding tests for solving the basic TSP problem
  + Ensured syntax is correct with isort and pep.
  + Make sure Travis CI builds all succeed
  + I modified the code from Google OR for computing the distance matrix. It was creating a dictionary, but the mip example just used a regular list of lists. It made more sense to initialize a numpy.zeros array and fill in the distances with integer indexing.



