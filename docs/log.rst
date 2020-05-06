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
  + Branch and Cut is the current record holder for the TSP, `solving a problem with 85,900 cities <https://en.wikipedia.org/wiki/Travelling_salesman_problem#Computing_a_solution>`_.
  + Allows defining a custom objective function, which will satisfy both problems
  + Implemented preliminary solution working and corresponding tests for solving the basic TSP problem
  + Ensured syntax is correct with isort and pep.
  + Make sure Travis CI builds all succeed
  + I modified the code from Google OR for computing the distance matrix. It was creating a dictionary, but the mip example just used a regular list of lists. It made more sense to initialize a numpy.zeros array and fill in the distances with integer indexing.

Day 4: 5/2/2020
################
+ Did some refactoring based on the tests from the python-pip library.
+ I am now indexing the nodes differently to make it more readable, in my opinion.
+ Having trouble with the second problem in the challenge (most nodes, fixed distance). The algorithm I am using is returning a non-contiguous path. Posted a `question on github <https://github.com/coin-or/python-mip/issues/96>`_. Will potentially add a test for this.
+ After trying for the full day, I decided to implement my own `nearest-nieghbors algorithm <https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm>`_ for the second solution. Was able to complete in a couple of hours, but it's a brute force approach. Will add tests and refactor tomorrow.
+ Also sent in a question about whether the solution for the second problem needs to be a closed loop or not.

Day 5: 5/3/2020
################
+ There are a lot of things I could do next, in roughly this order of priority:

  + Clean up code and get it ready for production

    + refactor nearest_neighbors
    + clean up and finalize branch_and_cut
    + document code
    + figure out best way to return render solution routes
    + write tests

  + write CLI
  + Create a Dockerfile for deployment as an API
  + Visualize routes with networkx
  + Parallelize nearest_neighbour_algorithm with dash

+ Refactoring the nearest_neighbors algorithm took a lot longer than expected.
+ I added the ability to find a feasible solution for the TSP using nearest neighbors.
+ I also refactored how to process the results. I am now using a matrix representing the edges used in the solution. This way, the output for the branch_and_cut method and the nearest_neighbors method are the same.
+ I did some testing and np.zeros in computing the euclidian matrix did not improve speed, so I initialized a list of lists full of zeros with a list comprehension.
+ I added a scaling feature to the distance matrix because rounding can cause problems.
+ Found an edge case for the nearest neighbors. If there is more than one nearest neighbor, check to make sure they have not been visited before.
+ Next step is to go from coordinates to solution. Currently, can go from coordinates to matrix, then matrix to solution, but I don't have test data to do both at once.

Day 6: 5/4/2020
################
+ Got everything working.
+ I made the distance constrained solution return a closed loop, but then found out that an open-loop was okay. That causes some issues in my implementation. They way I was generating the route from the route_matrix couldn't handle an open loop. I was able to fix it to allow both open and closed loops in a route_matrix.
+ Added tests for both open and closed loops.
+ Added test data from the `Google OR-Tools example <https://developers.google.com/optimization/routing/tsp#or-tools>`_ to go from coordinates to a solution.
+ The branch_and_cut algorithm does not respect the max_seconds argument for some reason, could be a problem with the library I am using. I discovered then when trying to solve the problem with the Google OR-Tools data.
+ Since the max_seconds argument doesn't work, I provided an initial feasible solution to the branch_and_cut algorithm using the nearest_neighbors algorithm. This guarantees a solution can be found, even if it is not the optimal solution.

Day 7: 5/5/2020
################
+ Cleaned up tests and logic
+ Found an edge case where max distance set to zero results in the route being one node going to itself. This is applicable if there are no solutions that meet the requirements.
+ Created the CLI and tests for the cLI. It creates a temporary CSV file and runs it with and without a max distance


