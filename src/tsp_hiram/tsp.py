from itertools import product
import math
from typing import (
    Dict,
    List,
    Iterator,
    NamedTuple,
    Set,
    Tuple,
    Union,
)

import numpy as np
from mip import (
    BINARY,
    minimize,
    Model,
    Var,
    xsum,
)

Coordinate = Tuple[int, int]
CoordinatesVector = List[Coordinate]
DistanceMatrixDict = Dict[int, Dict[int, int]]
MipVarMatrix = List[List[Var]]


class RouteStop(NamedTuple):
    from_node: int
    to_node: int


def compute_euclidean_distance_matrix(coordinates: CoordinatesVector) -> DistanceMatrixDict:
    """Creates a matrix of euclidian distances between the coordinates. Modified from https://developers.google.com/optimization/routing/tsp#euclid_distance

    :param coordinates: A list of 2D coordinates
    :type coordinates: CoordinatesVector
    :return: [description]
    :rtype: DistanceMatrixDict
    """
    distances = np.zeros((len(coordinates), len(coordinates)))
    for from_counter, from_node in enumerate(coordinates):
        for to_counter, to_node in enumerate(coordinates):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                # Euclidean distance
                distances[from_counter][to_counter] = (int(
                    math.hypot((from_node[0] - to_node[0]),
                               (from_node[1] - to_node[1]))))
    return distances


def tour_generator(V: Set[int], x: MipVarMatrix, return_home=False) -> RouteStop:
    """Generator for finding the next node of a solution. The next node is where the column of the current row (from_node) is 1.0

    :param V: Set of vertices (nodes)
    :type V: Set
    :param x: Matrix of shape (len(V),len(V)) indicating whether the arc between two nodes is used in the solution
    :type x: MipVarMatrix
    :return: returns a tuple with the from and to nodes
    :rtype: NamedTuple
    """
    from_node = 0
    while True:
        to_node = [j for j in V if x[from_node][j].x >= 0.99][0]
        yield RouteStop(from_node, to_node)
        from_node = to_node
        if to_node == 0:
            break


def solve_problem(distance_matrix: DistanceMatrixDict) -> Iterator[RouteStop]:
    """Solves a distance matrix for the shortest path

    :param distance_matrix: Distance maxtrix such as returned from `compute_euclidean_distance_matrix`
    :type distance_matrix: DistanceMatrixDict
    :return:  A generator yielding each RouteStop in the tour solution
    :rtype: Iterator[RouteStop]
    :yield: NamedTuple with the from_node and to_node
    :rtype: RouteStop
    """
    n, V = len(distance_matrix), set(range(len(distance_matrix)))
    model = Model()

    # binary variables indicating if arc (i,j) is used on the route or not
    x = [[model.add_var(var_type=BINARY) for j in V] for i in V]

    # continuous variable to prevent subtours: each city will have a
    # different sequential id in the planned route except the first one
    y = [model.add_var() for i in V]

    # objective function: minimize the distance
    model.objective = minimize(xsum(distance_matrix[i][j]*x[i][j] for i in V for j in V))

    # constraint : leave each city only once
    for i in V:
        model += xsum(x[i][j] for j in V - {i}) == 1

    # constraint : enter each city only once
    for i in V:
        model += xsum(x[j][i] for j in V - {i}) == 1

    # subtour elimination
    for (i, j) in product(V - {0}, V - {0}):
        if i != j:
            model += y[i] - (n+1)*x[i][j] >= y[j]-n

    # optimizing
    model.optimize(max_seconds=30)

    return tour_generator(V, x)
