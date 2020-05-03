import random
import math
import logging

logging.basicConfig(level=logging.INFO)

N = ['Antwerp', 'Bruges', 'C-Mine', 'Dinant', 'Ghent',
     'Grand-Place de Bruxelles', 'Hasselt', 'Leuven',
     'Mechelen', 'Mons', 'Montagne de Bueren', 'Namur',
     'Remouchamps', 'Waterloo']

n, V = len(N), set(range(len(N)))

# distances in an upper triangular matrix
dists = [[83, 81, 113, 52, 42, 73, 44, 23, 91, 105, 90, 124, 57],
         [161, 160, 39, 89, 151, 110, 90, 99, 177, 143, 193, 100],
         [90, 125, 82, 13, 57, 71, 123, 38, 72, 59, 82],
         [123, 77, 81, 71, 91, 72, 64, 24, 62, 63],
         [51, 114, 72, 54, 69, 139, 105, 155, 62],
         [70, 25, 22, 52, 90, 56, 105, 16],
         [45, 61, 111, 36, 61, 57, 70],
         [23, 71, 67, 48, 85, 29],
         [74, 89, 69, 107, 36],
         [117, 65, 125, 43],
         [54, 22, 84],
         [60, 44],
         [97],
         []]


# distances matrix
distance_matrix = [[0 if i == j
                    else dists[i][j-i-1] if j > i
                    else dists[j][i-j-1]
                    for j in V] for i in V]


def get_shortest_edge(i, visited, distance_matrix):
    return min([distance_matrix[i][j] for j in V if visited[i][j] == False])

max_distance = 90

def nearest_neighbor_path(distance_matrix, start: int = None, max_distance: int = None) -> List:
    """[summary]

    :param distance_matrix: Simple nearest neighbor algorithm for finding a feasable path for the Traveling Salesman Problem.
    :type distance_matrix: List
    :param start: The node to start to search for a solution, defaults to a randomly chosen node
    :type start: int, optional
    :param max_distance: The maximium distance of the path. If not specific, will find a full path. Otherwise, it will constrain the total cost of the path to be less than or equal to max_distance, defaults to None
    :type max_distance: int, optional
    :return: A feasable solution for the path satisfying the parameters provided.
    :rtype: List
    """


    if start == None:
        start = random.randrange(0, len(distance_matrix))
        logging.info(f'Choosing random starting node: {start}.')

    if max_distance == None:
        max_distance = math.inf

    i = start
    route = [i]

    # Initialize all vertices as unvisited except for self
    visited = [False for v in range(len(distance_matrix))]
    visited[start] = True
    nodes_visited = 1

    distance = 0
    while distance <= max_distance:

        # Have we visited all the nodes?
        if sum(visited) == len(visited):
            distance += distance_matrix[i][start]
            break

        else:
            # Find out the shortest edge connecting the current vertex u and an unvisited vertex v
            shortest_edge = min([distance_matrix[i][j] for j in V if visited[j] == False])

            # can we get home?
            go_home_cost = distance_matrix[i][start]
            if distance + go_home_cost + shortest_edge >= max_distance:
                logging.info(f'lets go home: {distance} + {go_home_cost}')
                distance += go_home_cost
                break

            else:
                distance += shortest_edge
                nearest = [j for j in V if distance_matrix[i][j] == shortest_edge]
                j = nearest[0]

                if len(nearest) > 1:
                    j = random.choice(nearest)
                    logging.info(f'Warning: more than one nearest neighbor for ({i},{j}). Choosing randomly.')

                nodes_visited += 1
                visited[j] = True
                route.append(j)
                i = j

    logging.info(f'{len(route)} nodes visited for distance {distance}: {route}')
    return route


for vertex in V:
    route = nearest_neighbor_path(distance_matrix, start=vertex)