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


def nearest_neighbor_path(start, max_distance, distance_matrix):
    distance = 0

    # Initialize all vertices as unvisited.
    visited = [[True if i==j else False for j in V] for i in V]

    i = start
    route = [i]
    nodes_visited = 1

    while distance <= max_distance:
        print(f'current_distance: {distance}')
        # Find out the shortest edge connecting the current vertex u and an unvisited vertex v.
        shortest_edge = get_shortest_edge(i, visited, distance_matrix)

        # can we get home?
        go_home_cost = distance_matrix[i][start]
        if distance + go_home_cost + shortest_edge  >= max_distance:
            print(f'lets go home: {distance} + {go_home_cost}')
            distance += go_home_cost
            break
        else:

            distance += shortest_edge
            nearest = [j for j in V if distance_matrix[i][j] == shortest_edge]
            if len(nearest) > 1:
                print(f'Warning: more than one nearest neighbor for ({i},{j}')
            j = nearest[0]
            nodes_visited += 1
            visited[i][j] = visited[j][i] = True


            i = j
            route.append(i)

    print(f'{len(route)} nodes visited for distance {distance}: {route}')
    return route

for vertex in V:
    nearest_neighbor_path(vertex, 90, distance_matrix)
