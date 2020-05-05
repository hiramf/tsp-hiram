import math

import numpy as np
import random
import pytest

from tsp_hiram import tsp


@pytest.fixture
def coordinates_google(scope="module"):
    data = [
        (288, 149), (288, 129), (270, 133), (256, 141), (256, 157), (246, 157),
        (236, 169), (228, 169), (228, 161), (220, 169), (212, 169), (204, 169),
        (196, 169), (188, 169), (196, 161), (188, 145), (172, 145), (164, 145),
        (156, 145), (148, 145), (140, 145), (148, 169), (164, 169), (172, 169),
        (156, 169), (140, 169), (132, 169), (124, 169), (116, 161), (104, 153),
        (104, 161), (104, 169), (90, 165), (80, 157), (64, 157), (64, 165),
        (56, 169), (56, 161), (56, 153), (56, 145), (56, 137), (56, 129),
        (56, 121), (40, 121), (40, 129), (40, 137), (40, 145), (40, 153),
        (40, 161), (40, 169), (32, 169), (32, 161), (32, 153), (32, 145),
        (32, 137), (32, 129), (32, 121), (32, 113), (40, 113), (56, 113),
        (56, 105), (48, 99), (40, 99), (32, 97), (32, 89), (24, 89),
        (16, 97), (16, 109), (8, 109), (8, 97), (8, 89), (8, 81),
        (8, 73), (8, 65), (8, 57), (16, 57), (8, 49), (8, 41),
        (24, 45), (32, 41), (32, 49), (32, 57), (32, 65), (32, 73),
        (32, 81), (40, 83), (40, 73), (40, 63), (40, 51), (44, 43),
        (44, 35), (44, 27), (32, 25), (24, 25), (16, 25), (16, 17),
        (24, 17), (32, 17), (44, 11), (56, 9), (56, 17), (56, 25),
        (56, 33), (56, 41), (64, 41), (72, 41), (72, 49), (56, 49),
        (48, 51), (56, 57), (56, 65), (48, 63), (48, 73), (56, 73),
        (56, 81), (48, 83), (56, 89), (56, 97), (104, 97), (104, 105),
        (104, 113), (104, 121), (104, 129), (104, 137), (104, 145), (116, 145),
        (124, 145), (132, 145), (132, 137), (140, 137), (148, 137), (156, 137),
        (164, 137), (172, 125), (172, 117), (172, 109), (172, 101), (172, 93),
        (172, 85), (180, 85), (180, 77), (180, 69), (180, 61), (180, 53),
        (172, 53), (172, 61), (172, 69), (172, 77), (164, 81), (148, 85),
        (124, 85), (124, 93), (124, 109), (124, 125), (124, 117), (124, 101),
        (104, 89), (104, 81), (104, 73), (104, 65), (104, 49), (104, 41),
        (104, 33), (104, 25), (104, 17), (92, 9), (80, 9), (72, 9),
        (64, 21), (72, 25), (80, 25), (80, 25), (80, 41), (88, 49),
        (104, 57), (124, 69), (124, 77), (132, 81), (140, 65), (132, 61),
        (124, 61), (124, 53), (124, 45), (124, 37), (124, 29), (132, 21),
        (124, 21), (120, 9), (128, 9), (136, 9), (148, 9), (162, 9),
        (156, 25), (172, 21), (180, 21), (180, 29), (172, 29), (172, 37),
        (172, 45), (180, 45), (180, 37), (188, 41), (196, 49), (204, 57),
        (212, 65), (220, 73), (228, 69), (228, 77), (236, 77), (236, 69),
        (236, 61), (228, 61), (228, 53), (236, 53), (236, 45), (228, 45),
        (228, 37), (236, 37), (236, 29), (228, 29), (228, 21), (236, 21),
        (252, 21), (260, 29), (260, 37), (260, 45), (260, 53), (260, 61),
        (260, 69), (260, 77), (276, 77), (276, 69), (276, 61), (276, 53),
        (284, 53), (284, 61), (284, 69), (284, 77), (284, 85), (284, 93),
        (284, 101), (288, 109), (280, 109), (276, 101), (276, 93), (276, 85),
        (268, 97), (260, 109), (252, 101), (260, 93), (260, 85), (236, 85),
        (228, 85), (228, 93), (236, 93), (236, 101), (228, 101), (228, 109),
        (228, 117), (228, 125), (220, 125), (212, 117), (204, 109), (196, 101),
        (188, 93), (180, 93), (180, 101), (180, 109), (180, 117), (180, 125),
        (196, 145), (204, 145), (212, 145), (220, 145), (228, 145), (236, 145),
        (246, 141), (252, 125), (260, 129), (280, 133)
    ]

    return data

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

def test_distance_matrix():
    """Test that computing distances from coordinates gives expected output.
    """
    coordinates = [(288, 149), (288, 129), (270, 133)]
    edm = tsp.compute_euclidean_distance_matrix(coordinates)
    assert edm == [
        [0, 20, 24],
        [20, 0, 18],
        [24, 18, 0],
    ]

def test_branch_and_cut(distance_matrix_mip):
    """Test the correct solution is returned from the branch and cut algorithm. Can be forwards or backwards (Note: Using nearest_neighbors for an initial feasable solution results in the best solution being returned in a reverse order from without using an initial feasable solution).
    """
    best_route = [8, 7, 6, 2, 10, 12, 3, 11, 9, 13, 5, 4, 1, 0]
    route_matrix, distance=tsp.branch_and_cut(distance_matrix_mip)
    tour= [edge[0] for edge in tsp.get_edges_from_route_matrix(route_matrix)]
    assert tour  in [best_route, best_route[::-1]] #
    assert int(distance) == 547

def test_nearest_neighbor_full_route(distance_matrix_mip):
    """Tests that the nearest neighbor algorithm finds the best possible route when iterating over each node as a starting point.
    """
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

@pytest.mark.parametrize("max_distance", [100, None])
@pytest.mark.parametrize("closed", [True, False])
def test_same_result(coordinates_google, max_distance, closed):
    """Tests constrained and non-constrained problems with open and closed loops using the google data.
    """
    distance_matrix = tsp.compute_euclidean_distance_matrix(random.sample(coordinates_google, 10))
    rm_optimize, distance_optimize = tsp.optimize(distance_matrix, max_distance=max_distance, closed=closed)