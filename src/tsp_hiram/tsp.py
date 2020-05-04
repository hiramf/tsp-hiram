import logging
import math
import random
from itertools import product
from typing import Dict, Iterator, List, NamedTuple, Set, Tuple

import numpy as np
from mip import BINARY, Model, Var, maximize, minimize, xsum

logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s', level=logging.DEBUG)

Coordinate = Tuple[int, int]
CoordinatesVector = List[Coordinate]
Matrix = List[List[int]]
MipVarMatrix = List[List[Var]]


class RouteStop(NamedTuple):
    from_node: int
    to_node: int


def compute_euclidean_distance_matrix(coordinates: CoordinatesVector) -> Matrix:
    """Creates a matrix of euclidian distances between the coordinates.
    Modified from https://developers.google.com/optimization/routing/tsp#euclid_distance

    :param coordinates: A list of 2D coordinates
    :type coordinates: CoordinatesVector
    :return: 2D matrix of euclidean distance between each coordinate
    :rtype: Matrix
    """
    V = range(len(coordinates))
    distances = [[0 for j in V] for i in V]
    for from_counter, from_node in enumerate(coordinates):
        for to_counter, to_node in enumerate(coordinates):
            if from_counter == to_counter:
                pass
            else:
                # Euclidean distance
                distances[from_counter][to_counter] = (int(
                    math.hypot((from_node[0] - to_node[0]),
                               (from_node[1] - to_node[1]))))
    return distances


def get_edges_from_route_matrix(route_matrix: Matrix) -> Tuple:
    """Generator which returns the next node in a route

    :param route_matrix: A matrix indicating which edges contain the optimal route
    :type route_matrix: Matrix
    :return: The row and column for the edge in the matrix
    :rtype: Tuple
    :yield: Generator which iteratively finds each subsequent node
    :rtype: Iterator[Tuple]
    """
    def get_next_node_from_row(i, route_matrix):
        for j in range(len(route_matrix)):
            if route_matrix[i][j] == 1:
                return (i,j)
        raise ValueError(f"Node {i} is not connected to another node.")

    edges = []
    route_length = np.sum(route_matrix)
    row = 0

    while len(edges) < route_length:
        try:
            to_node = get_next_node_from_row(row, route_matrix)
            row = to_node[1]
            edges.append(to_node)
        except ValueError:
            row += 1

    return edges


def branch_and_cut(distance_matrix: Matrix, max_seconds=20) -> Tuple[Matrix, int]:
    """Solves a distance matrix for the shortest path

    :param distance_matrix: Distance maxtrix such as returned from `compute_euclidean_distance_matrix`
    :type distance_matrix: Matrix
    :param max_seconds: The max execution time in seconds
    :type max_seconds: int
    :return:  A matrix indicating which edges contain the optimal route, the distance of the route
    :rtype: Tuple[Matrix, int]
    """
    n = len(distance_matrix)
    model = Model()
    model.verbose=0

    # binary variables indicating if arc (i,j) is used on the route or not
    x = [[model.add_var(name=f'x({i},{j})', var_type=BINARY) for j in range(n)] for i in range(n)]

    # continuous variable to prevent subtours: each city will have a
    # different sequential id in the planned route except the first one
    y = [model.add_var(name=f'y({i})') for i in range(n)]

    # objective function: minimize the distance
    model.objective = minimize(xsum(distance_matrix[i][j]*x[i][j] for i in range(n) for j in range(n)))

    # constraint : enter each city coming from another city
    for i in range(n):
        model += xsum(x[j][i] for j in range(n) if j != i) == 1

    # constraint : leave each city coming from another city
    for i in range(n):
        model += xsum(x[i][j] for j in range(n) if j != i) == 1

    # subtour elimination
    for i in range(1, n):
        for j in [x for x in range(1, n) if x != i]:
            model += y[i] - (n+1)*x[i][j] >= y[j]-n, 'noSub({},{})'.format(i, j)

    # optimizing
    model.optimize(max_seconds=max_seconds)
    logging.info(f'Best route found has length {model.objective_value}.')

    route_matrix = [[int(x[i][j].x) for j in range(n)] for i in range(n)]
    return route_matrix, model.objective_value


def nearest_neighbor_path(distance_matrix, start: int = None, max_distance: int = None) -> Tuple[Matrix, int]:
    """Simple nearest neighbor algorithm for finding a feasable path for the Traveling Salesman Problem.

    :param distance_matrix: matrix for the cost of each edge
    :type distance_matrix: List
    :param start: The node to start to search for a solution, defaults to a randomly chosen node
    :type start: int, optional
    :param max_distance: The maximium distance of the path. If not specific, will find a full path. Otherwise, it will constrain the total cost of the path to be less than or equal to max_distance, defaults to None
    :type max_distance: int, optional
    :return:  A matrix indicating which edges contain the optimal route, the distance of the route
    :rtype: Tuple[Matrix, int]
    """

    n = len(distance_matrix)

    if start == None:
        start = random.randrange(0, len(distance_matrix))
        logging.info(f'Choosing random starting node: {start}.')

    if max_distance == None:
        max_distance = math.inf

    # Initialize all vertices as unvisited except for self
    visited = [False for v in range(n)]
    visited[start] = True

    route = [start]

    route_matrix = [[0 for j in range(n)] for i in range(n)]

    from_node = start
    distance = 0
    while distance <= max_distance:

        # Have we visited all the nodes?
        if sum(visited) == len(visited):
            # then let's go home
            distance += distance_matrix[from_node][start]
            route_matrix[from_node][start] = 1
            break

        # Find out the shortest edge connecting the current vertex and an unvisited vertex
        shortest_edge = min([distance_matrix[from_node][to_node] for to_node in range(n) if visited[to_node] == False])
        next_nodes = [node for node in range(n) if distance_matrix[from_node][node] == shortest_edge]
        next_nodes = [node for node in next_nodes if visited[node] == False]
        to_node = next_nodes[0]
        if len(next_nodes) > 1:
            # more than one nearest neighbor, choosing randomly
            logging.info('more than one neighor found.')
            to_node = random.choice(next_nodes)

        # do we have enough to get home if we go the next edge?
        go_home_cost = distance_matrix[to_node][start]
        if distance + go_home_cost + shortest_edge >= max_distance:
            # then let's go home
            distance += distance_matrix[from_node][start]
            route_matrix[from_node][start] = 1
            break

        else:
            # then keep going!
            distance += shortest_edge
            visited[to_node] = True
            route_matrix[from_node][to_node] = 1
            route.append(to_node)
            from_node = to_node

    logging.info(f'{sum(visited)} nodes visited for distance {distance}: {route}')
    return route_matrix, distance

def optimize(distance_matrix, max_distance=None, starting_node=None, max_seconds=20):

    # use nearest neighbors algorithm
    if max_distance:
        logging.info(f'Constraining solution to max distance {max_distance}')
        if starting_node:
            logging.info(f'Starting at node {starting_node}')
            route_matrix, distance = nearest_neighbor_path(distance_matrix, max_distance=max_distance, start = starting_node)

        else:
            # TODO: allow for returning multiple solutions if there is more than one. Currently only returns first solution that satisfies the constraint max_distance.
            most_nodes = 0
            route_matrix = None
            distance = None
            for vertex in range(len(distance_matrix)):
                _route_matrix, _distance = nearest_neighbor_path(distance_matrix, max_distance = max_distance, start = vertex)
                logging.info(f'Solution: {n_nodes} for {distance} from start {vertex}')
                n_nodes = np.sum(_route_matrix)

                if n_nodes > most_nodes:
                    most_nodes = n_nodes
                    route_matrix = _route_matrix
                    distance = _distance

    else:
        route_matrix, distance = branch_and_cut(distance_matrix)

    return route_matrix, distance
