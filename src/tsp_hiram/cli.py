import argparse
import csv

from tsp_hiram import tsp

parser = argparse.ArgumentParser(description='Solve Traveling Salesman Problem given a list of coordinates')
parser.add_argument('filename', metavar='FILENAME', type=str, help="File containing the coordinates.")
parser.add_argument('--max', type=int, default=None, help='Max distance of the route')
parser.add_argument('--closed', type=bool, default=False, help='Whether a constrained solutions should be an open or closed loop')


def main(args=None):
    args = parser.parse_args(args=args)
    with open(args.filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # TODO: More robust handling of csvreader. Currently just drops first row as header and makes a lot of assumptions
        coordinates = [(int(x), int(y)) for [x, y] in [row for row in reader][1:]]
        route, distance = tsp.optimize(coordinates, max_distance=args.max, closed=args.closed)

        if args.max is not None:
            print(f'{len(route)} nodes could be touched with max distance of {args.max}')
        else:
            print(f'Solution with distance of {distance} found: {route}')

        return route, distance
