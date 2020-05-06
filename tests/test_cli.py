import csv
import sys

import pytest

from tsp_hiram.cli import main


@pytest.fixture
def coordinates_list():
    data = [
        [8, 41],
        [220, 125],
        [56, 89],
        [196, 145],
        [196, 49],
        [64, 21],
        [124, 117],
        [212, 65],
        [24, 17],
        [24, 25],
        [172, 117],
        [260, 109],
        [252, 21],
        [172, 145],
        [40, 137],
    ]

    return data


@pytest.mark.parametrize("max_distance,expected", [(None, 750), (100, 88)])
def test_main(monkeypatch, tmp_path, coordinates_list, max_distance, expected):
    """Tests the CLI with and without max distance parameter
    """
    # Create a temporary file called "coordinates.csv"
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "coordinates.csv"
    filepath = str(p)
    with open(p, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(['x', 'y'])
        for row in coordinates_list:
            writer.writerow(row)

    # Test the CLI with different args
    with monkeypatch.context() as m:
        args = ['main', filepath]
        if max_distance is not None:
            args += ['--max', str(max_distance)]
        m.setattr(sys, 'argv', args)
        route, distance = main()
        assert distance == expected
