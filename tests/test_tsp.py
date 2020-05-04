import math

import numpy as np
import pytest

from tsp_hiram import tsp


def test_distance_matrix():
    coordinates = [(288, 149), (288, 129), (270, 133)]
    edm = tsp.compute_euclidean_distance_matrix(coordinates)
    assert edm == [
        [0, 20, 24],
        [20, 0, 18],
        [24, 18, 0],
    ]

@pytest.fixture
def distance_matrix_mip(scope="module"):
    distances = [
        [0, 83, 81, 113, 52, 42, 73, 44, 23, 91, 105, 90, 124, 57],
        [83, 0, 161, 160, 39, 89, 151, 110, 90, 99, 177, 143, 193, 100],
        [81, 161, 0, 90, 125, 82, 13, 57, 71, 123, 38, 72, 59, 82],
        [113, 160, 90, 0, 123, 77, 81, 71, 91, 72, 64, 24, 62, 63],
        [52, 39, 125, 123, 0, 51, 114, 72, 54, 69, 139, 105, 155, 62],
        [42, 89, 82, 77, 51, 0, 70, 25, 22, 52, 90, 56, 105, 16],
        [73, 151, 13, 81, 114, 70, 0, 45, 61, 111, 36, 61, 57, 70],
        [44, 110, 57, 71, 72, 25, 45, 0, 23, 71, 67, 48, 85, 29],
        [23, 90, 71, 91, 54, 22, 61, 23, 0, 74, 89, 69, 107, 36],
        [91, 99, 123, 72, 69, 52, 111, 71, 74, 0, 117, 65, 125, 43],
        [105, 177, 38, 64, 139, 90, 36, 67, 89, 117, 0, 54, 22, 84],
        [90, 143, 72, 24, 105, 56, 61, 48, 69, 65, 54, 0, 60, 44],
        [124, 193, 59, 62, 155, 105, 57, 85, 107, 125, 22, 60, 0, 97],
        [57, 100, 82, 63, 62, 16, 70, 29, 36, 43, 84, 44, 97, 0]
    ]

    return distances


def test_branch_and_cut(distance_matrix_mip):
    route_matrix, distance=tsp.branch_and_cut(distance_matrix_mip)
    tour=tsp.get_edges_from_route_matrix(route_matrix)
    assert tour == [(0, 8), (8, 7), (7, 6), (6, 2), (2, 10), (10, 12), (12, 3), (3, 11), (11, 9), (9, 13), (13, 5), (5, 4), (4, 1), (1, 0)]
    assert int(distance) == 547

def test_nearest_neighbor_full_route(distance_matrix_mip):
    best_distance=math.inf
    best_route=None

    for vertex in range(len(distance_matrix_mip)):
        route_matrix, distance=tsp.nearest_neighbor_path(distance_matrix_mip, start = vertex)

        assert np.sum(route_matrix) == len(distance_matrix_mip)

        if distance < best_distance:
            best_distance=distance
            best_route=route_matrix

    assert tsp.get_edges_from_route_matrix(best_route) == [(0, 8), (8, 5), (5, 13), (13, 7),
                                           (7, 6), (6, 2), (2, 10), (10, 12), (12, 11), (11, 3), (3, 9), (9, 4), (4, 1), (1, 0)]


def test_optimize_branch_and_cut(distance_matrix_mip):
    route_matrix, distance = tsp.optimize(distance_matrix_mip)
    tour=tsp.get_edges_from_route_matrix(route_matrix)
    assert tour == [(0, 8), (8, 7), (7, 6), (6, 2), (2, 10), (10, 12), (12, 3), (3, 11), (11, 9), (9, 13), (13, 5), (5, 4), (4, 1), (1, 0)]
    assert int(distance) == 547

@pytest.mark.parametrize("closed", [True, False])
@pytest.mark.parametrize("max_distance", [0, 50, 200, 10000])
def test_max_distance(distance_matrix_mip, closed, max_distance):
    """Test limiting a solution to a fixed distance for both open and closed loops for various distances.

    :param closed: Closed or open loop solution
    :type closed: bool
    :param max_distance: Maximum distance for the solution
    :type max_distance: int
    """
    n = len(distance_matrix_mip)
    for i in range(n):
        route_matrix, distance = tsp.optimize(distance_matrix_mip, starting_node=i, max_distance=max_distance, closed=closed)
        route = [ edge[0] for edge in tsp.get_edges_from_route_matrix(route_matrix)]
        assert len(route) == len(set(route))
        assert distance <= max_distance