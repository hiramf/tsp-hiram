import math
from typing import List, Tuple, Dict
Coordinate = Tuple[int, int]
CoordinatesVector = List[Coordinate]
DistanceMatrixDict = Dict[int, Dict[int, int]]

def compute_euclidean_distance_matrix(coordinates: CoordinatesVector) -> DistanceMatrixDict:
    """
    Source: https://developers.google.com/optimization/routing/tsp#euclid_distance
    """
    distances = {}
    for from_counter, from_node in enumerate(coordinates):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(coordinates):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                # Euclidean distance
                distances[from_counter][to_counter] = (int(
                    math.hypot((from_node[0] - to_node[0]),
                               (from_node[1] - to_node[1]))))
    return distances

def solve_problem(distance_matrix: DistanceMatrixDict) -> List:
    return 0