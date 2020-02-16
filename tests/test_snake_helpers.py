from app.snake_helpers import *
from testing_tools import *


def test_hitWall():
    data = resetData(1)

    # print("should collide with wall, going up")
    redefineYou(data, [(6, 0)])
    assert hitWall(data, 'up') is True

    # print("should collide with wall, going left")
    redefineYou(data, [(0, 3)])
    assert hitWall(data, 'left') is True

    # print("should collide with wall, going right")
    redefineYou(data, [(data['board']['width'], 3)])
    assert hitWall(data, 'right') is True

    # print("should collide with wall, going down")
    redefineYou(data, [(6, data['board']['height'])])
    assert hitWall(data, 'down') is True

    # print("should not collide with wall, going up")
    redefineYou(data, [(6, data['board']['height'])])
    assert hitWall(data, 'up') is False


def test_hitSnake():
    data = resetData(2)

    # print("should not collide with snake, going right (tail)")
    assert hitSnake(data, 'right') is False

    # print("should collide with snake, going up")
    assert hitSnake(data, 'up') is True

    # print("should collide with SELF, going down")
    assert hitSnake(data, 'down') is True

    # print("should not collide with snake, going left (although off board)")
    assert hitSnake(data, 'left') is False


def test_possibleMoves():
    data = resetData(1)
    # print("should be able to move any direction")
    assert possibleMoves(data) == {'up', 'down', 'left', 'right'}

    data = resetData(2)
    # print("should be able to move left or right (tail is right)")
    assert possibleMoves(data) == {'left', 'right'}


def test_distHeadToWalls():
    data = resetData(1)
    head = data['you']['body'][0]
    w = data['board']['width']
    h = data['board']['height']

    assert distHeadToWalls(head, w, h) == {
        'up': 3,
        'down': 11,
        'left': 1,
        'right': 13
    }


def test_avoidEdges():
    data = resetData(1)
    # print("should avoid being next to wall (do not allow left)")
    possible = possibleMoves(data)
    assert avoidEdges(data, possible, 1) == {'up', 'down', 'right'}


def test_distance():
    a = (1,2)
    b = {'x': 3, 'y': 1}
    # print("should be 3")
    assert distance(a, b) == 3


def test_rateFood():
    data = resetData(1)
    # print("should be None (no food on board)")
    assert rateFood(data) is None

    data = resetData(2)
    # print("should be (0,1)")
    assert rateFood(data) == [((1, 5), 2), ((0, 1), 3), ((9, 9), 14)]


def test_nextMove():
    data = resetData(2)
    # print("should return a single move")
    print("nextMove", nextMove(data))


if __name__ == "__main__":
    test_hitWall()
    test_hitSnake()
    test_possibleMoves()
    test_distHeadToWalls()
    test_avoidEdges()
    test_nextMove()
    test_distance()
    test_rateFood()
