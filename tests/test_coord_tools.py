from app.coord_tools import *
from testing_tools import *


def test_dictToTuple():
    assert dictToTuple({'x': 1, 'y': 3}) == (1, 3)


def test_listDictToTuple():
    lst = [
        {'x': 1, 'y': 3},
        {'x': 0, 'y': 0}
    ]
    assert listDictToTuple(lst) == [(1, 3), (0, 0)]

    lst = []
    assert listDictToTuple(lst) == []


def test_goToPoint():
    data = resetData(1)
    # print("point is up and left of head")
    assert goToPoint(data, (0, 0)) == {'up', 'left'}

    # print("point is down and right of head")
    assert goToPoint(data, (9, 9)) == {'down', 'right'}


if __name__ == "__main__":
    test_dictToTuple()
    test_listDictToTuple()
    test_goToPoint()