import numpy as np
import pytest

from tsp_hiram import tsp


@pytest.fixture
def coordinates():
    return [(288, 149), (288, 129), (270, 133)]


@pytest.fixture
def distance_matrix():
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
def distance_matrix_mip():
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


def test_tour(distance_matrix_mip):
    tour = tsp.solve_problem(distance_matrix_mip)
    assert [0, 1, 4, 5, 13, 9, 11, 3, 12, 10, 2, 6, 7, 8] == [i.from_node for i in tour]
