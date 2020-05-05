import logging
import math
import random
from typing import List, Tuple

import numpy as np
from mip import BINARY, Model, OptimizationStatus, Var, minimize, xsum

logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s', level=logging.DEBUG)

Coordinate = Tuple[int, int]
CoordinatesVector = List[Coordinate]
Matrix = List[List[int]]


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

    def get_first_row(route_matrix):
        for row in range(len(route_matrix)):
            nodes_in_row = sum(route_matrix[row])
            if nodes_in_row == 1:
                return row
            elif nodes_in_row == 0:
                continue
            else:
                raise ValueError(f'Invalid number of nodes in row: {nodes_in_row}')

    def get_next_node_from_row(i, route_matrix):
        for j in range(len(route_matrix)):
            if route_matrix[i][j] == 1:
                return (i, j)
        raise ValueError(f"Node {i} is not connected to another node.")

    edges = []
    route_length = np.sum(route_matrix)
    row = get_first_row(route_matrix)

    while len(edges) < route_length:
        try:
            to_node = get_next_node_from_row(row, route_matrix)
            row = to_node[1]
            edges.append(to_node)
        except ValueError:
            logging.info('End of open route found.')
            # transpose the matrix
            route_matrix = [[route_matrix[j][i] for j in range(len(route_matrix))] for i in range(len(route_matrix))]
            # reverse the edges
            edges = [(edges[-1][1], edges[-1][0])]
            row = edges[0][1]
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

    # Use nearest neighbors to find an initial feasible solution
    feasible_rm, feasible_distance = nearest_neighbor_path(distance_matrix, closed=True)
    model.start = [(x[i][j], float(feasible_rm[i][j])) for i in range(n) for j in range(n)]

    # optimizing
    model.optimize(max_seconds=max_seconds)
    if model.status in [OptimizationStatus.OPTIMAL, OptimizationStatus.FEASIBLE]:
        logging.info(f'Best route found has length {model.objective_value}.')

        route_matrix = [[int(x[i][j].x) for j in range(n)] for i in range(n)]
        return route_matrix, model.objective_value

    else:
        logging.info('No solution found.')
        route_matrix = [[0 for j in range(n)] for i in range(n)]
        return route_matrix, 0


def nearest_neighbor_path(distance_matrix, closed=False, start: int = None, max_distance: int = None) -> Tuple[Matrix, int]:
    """Simple nearest neighbor algorithm for finding a feasible path for the Traveling Salesman Problem.

    :param distance_matrix: matrix for the cost of each edge
    :type distance_matrix: List
    :param start: The node to start to search for a solution, defaults to a randomly chosen node
    :type start: int, optional
    :param max_distance: If None, find full path. Otherwise, constrain cost of the path to be >= max_distance, defaults to None
    :type max_distance: int, optional
    :return:  A matrix indicating which edges contain the optimal route, the distance of the route
    :rtype: Tuple[Matrix, int]
    """

    n = len(distance_matrix)

    if start is None:
        start = random.randrange(0, len(distance_matrix))
        logging.info(f'Choosing random starting node: {start}.')

    if max_distance is None:
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
        shortest_edge = min([distance_matrix[from_node][to_node] for to_node in range(n) if visited[to_node] is False])

        next_nodes = [node for node in range(n) if distance_matrix[from_node][node] == shortest_edge]
        next_nodes = [node for node in next_nodes if visited[node] is False]
        to_node = next_nodes[0]
        go_home_cost = distance_matrix[to_node][start] + shortest_edge

        if len(next_nodes) > 1:
            # more than one nearest neighbor, choosing randomly
            logging.info('more than one neighor found.')
            to_node = random.choice(next_nodes)

        # do we have enough to get home if we go the next edge?
        if closed & (distance + go_home_cost >= max_distance):
            # then let's go home
            distance += distance_matrix[from_node][start]
            route_matrix[from_node][start] = 1
            break

        elif distance + shortest_edge >= max_distance:
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


def optimize(distance_matrix, max_distance=None, starting_node=None, max_seconds=20, closed=True, use_nearest_neighbors=False):
    """[summary]

    :param distance_matrix: [description]
    :type distance_matrix: [type]
    :param max_distance: [description], defaults to None
    :type max_distance: [type], optional
    :param starting_node: [description], defaults to None
    :type starting_node: [type], optional
    :param max_seconds: [description], defaults to 20
    :type max_seconds: int, optional
    :param closed: [description], defaults to True
    :type closed: bool, optional
    :param use_nearest_neighbors: [description], defaults to False
    :type use_nearest_neighbors: bool, optional
    :return: [description]
    :rtype: [type]
    """
    assert len(distance_matrix) == len(distance_matrix[0]), "Invalid distance matrix. Must be 2D square."

    # use nearest neighbors algorithm
    if (max_distance is not None) or (use_nearest_neighbors is True):
        logging.info('Max seconds is specified but not supported for nearest neighbors algorithm.')

        logging.info(f'Constraining solution to max distance {max_distance}')
        if starting_node:
            logging.info(f'Starting at node {starting_node}')
            route_matrix, distance = nearest_neighbor_path(distance_matrix, max_distance=max_distance, start=starting_node, closed=closed)

        else:
            # TODO: allow for returning multiple solutions if there is more than one.
            most_nodes = 0
            route_matrix = None
            distance = None
            for vertex in range(len(distance_matrix)):
                _route_matrix, _distance = nearest_neighbor_path(distance_matrix, max_distance=max_distance, start=vertex, closed=closed)
                logging.info(f'Solution: {np.sum(_route_matrix)} for {distance} from start {vertex}')
                n_nodes = np.sum(_route_matrix)

                if n_nodes >= most_nodes:
                    most_nodes = n_nodes
                    route_matrix = _route_matrix
                    distance = _distance

    else:
        if closed is False:
            logging.info('Closed loop argument is False but no max distance is specified. Running branch and cut.')
        route_matrix, distance = branch_and_cut(distance_matrix, max_seconds=max_seconds)

    return route_matrix, distance
