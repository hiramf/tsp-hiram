import pytest
from tsp_hiram import tsp

@pytest.fixture
def coordinates():
    return [(288,149), (288,129), (270,133)]

@pytest.fixture
def distance_matrix():
    return {
        0: {0: 0, 1: 20, 2: 24},
        1: {0: 20, 1: 0, 2: 18},
        2: {0: 24, 1: 18, 2: 0}
        }

def test_distance_matrix(coordinates, distance_matrix):
    edm = tsp.compute_euclidean_distance_matrix(coordinates)
    print(edm)
    assert edm == distance_matrix

def test_tour(distance_matrix):
    tour = tsp.solve_problem(distance_matrix)
    assert tour == [0,1,3,2]