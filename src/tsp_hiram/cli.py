"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mtsp_hiram` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``tsp_hiram.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``tsp_hiram.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse
import csv

from tsp_hiram import tsp

parser = argparse.ArgumentParser(description='Solve Traveling Salesman Problem given a list of coordinates')
parser.add_argument('filename', metavar='FILENAME', type=str, help="File containing the coordinates.")
parser.add_argument('--max', type=int, default=None, help='Max distance of the path')


def main(args=None):
    args = parser.parse_args(args=args)
    with open(args.filename, newline='') as csvfile:
      reader = csv.reader(csvfile, delimiter = ',')
      # TODO: More robust handling of csvreader. Currently just drops first row as header and makes a lot of assumptions
      coordinates = [(int(x), int(y)) for [x,y] in [row for row in reader][1:]]
      route, distance = tsp.optimize(coordinates, max_distance=args.max)
      print(f'Solution with distance of {distance} found: {route}')
      return route, distance


