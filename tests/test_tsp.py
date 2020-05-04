import numpy as np
import pytest

from tsp_hiram import tsp

@pytest.fixture
def coordinates():
    return [(288, 149), (288, 129), (270, 133)]


@pytest.fixture
def distance_matrix(scope="module"):
    distances = np.array([
        [0, 20, 24],
        [20, 0, 18],
        [24, 18, 0],
    ])
    return distances


def test_distance_matrix(coordinates, distance_matrix):
    edm = tsp.compute_euclidean_distance_matrix(coordinates)
    np.testing.assert_array_equal(edm, distance_matrix)


@pytest.fixture
def distance_matrix_mip(scope="module"):
    distances = np.array(
        [[0, 83, 81, 113, 52, 42, 73, 44, 23, 91, 105, 90, 124, 57],
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
            [57, 100, 82, 63, 62, 16, 70, 29, 36, 43, 84, 44, 97, 0]]
    )
    return distances


def test_branch_and_cut(distance_matrix_mip):
    route_matrix, distance = tsp.branch_and_cut(distance_matrix_mip)
    tour = tsp.get_edges_from_route_matrix(route_matrix)
    assert [i[0] for i in tour] == [0, 8, 7, 6, 2, 10, 12, 3, 11, 9, 13, 5, 4, 1]
    assert int(distance) == 547

def test_nearest_neighbor_max_distance(distance_matrix_mip):
    best_distance = 0
    best_route = None

    for vertex in range(len(distance_matrix_mip)):
        route_matrix, distance = tsp.nearest_neighbor_path(
            distance_matrix_mip,
            max_distance=200,
            start=vertex)

        if distance > best_distance:
            best_distance = distance
            best_route = route_matrix

    assert best_distance == 199
    assert tsp.get_edges_from_route_matrix(best_route) == [(0, 8), (8, 4), (4, 1), (1, 0)]