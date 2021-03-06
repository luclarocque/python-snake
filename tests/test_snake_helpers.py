from app.snake_helpers import *
from tests.testing_tools import *
from tests.visualize_board import visualize


def test_hitWall():
    data = resetData(1)
    head = getHead(data)

    # print("should collide with wall, going up")
    assert hitWall(data, (6, 0), 'up') is True

    # print("should collide with wall, going left")
    assert hitWall(data, (0, 3), 'left') is True

    # print("should collide with wall, going right")
    assert hitWall(data, (14, 3), 'right') is True

    # print("should collide with wall, going down")
    assert hitWall(data, (6, 14), 'down') is True

    # print("should not collide with wall, going up")
    assert hitWall(data, (6, 14), 'up') is False


def test_hitSnake():
    data = resetData(2)
    head = getHead(data)

    # print("should not collide with snake, going right (tail)")
    assert hitSnake(data, head, 'right') is False

    # print("should collide with snake, going up")
    assert hitSnake(data, head, 'up') is True

    # print("should collide with SELF, going down")
    assert hitSnake(data, head, 'down') is True

    # print("should not collide with snake, going left (although off board)")
    assert hitSnake(data, head, 'left') is False


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
    assert avoidEdges(data, 1) == {'up', 'down', 'right'}


def test_distance():
    a = (1, 2)
    b = {'x': 3, 'y': 1}
    # print("should be 3")
    assert distance(a, b) == 3


def test_rateFood():
    data = resetData(1)
    # print("should be None (no food on board)")
    assert getFoodDistList(data) is None

    data = resetData(2)
    # print("should return ordered list with nearest food first")
    assert getFoodDistList(data) == [((1, 5), 2), ((0, 1), 3), ((9, 9), 14)]


def test_goToFood():
    data = resetData(3)
    print("should return {up, right} despite right being impossible: hit self")
    assert getFoodMoves(data) == {'up', 'right'}


def test_getFloodSizeList():
    data = resetData(4)
    # print("should only have non-zero size for left and right")
    snakeMap = mapSnakes(data)
    floodSizeList = getFloodSizeList(data, snakeMap)
    print("floodSizeList", floodSizeList)
    assert floodSizeList == [('right', 89),
                             ('left', 1)]


def test_avoidHeadMoves():
    data = resetData(4)
    # print("only head nearby is of smaller snake, so target by going right")
    headMap = getHeadMap(data)
    assert avoidHeadMoves(data, headMap) == {'right'}

    data = resetData(5)
    # print("nearby snake is larger, so must go down to avoid head")
    headMap = getHeadMap(data)
    assert avoidHeadMoves(data, headMap) == {'down'}


def test_nextMove():
    data = resetData(2)
    assert not hitAny(data, getHead(data), nextMove(data))
    #
    data = resetData(3)
    assert not hitAny(data, getHead(data), nextMove(data))
    #
    data = resetData(4)
    # visualize(data)
    assert not hitAny(data, getHead(data), nextMove(data))
    #
    data = resetData(5)
    # visualize(data)
    assert not hitAny(data, getHead(data), nextMove(data))
    #
    data = resetData(6)
    # visualize(data)
    assert not hitAny(data, getHead(data), nextMove(data))
    #
    data = resetData(7)
    # visualize(data)
    assert not hitAny(data, getHead(data), nextMove(data))
    #
    data = resetData(8)
    # visualize(data)
    assert not hitAny(data, getHead(data), nextMove(data))
    #
    data = resetData(9)
    # visualize(data)
    assert not hitAny(data, getHead(data), nextMove(data))

    data = resetData(10)
    # visualize(data)
    assert not hitAny(data, getHead(data), nextMove(data))


if __name__ == "__main__":
    test_nextMove()
    test_hitWall()
    test_hitSnake()
    test_possibleMoves()
    test_distHeadToWalls()
    test_avoidEdges()
    test_nextMove()
    test_distance()
    test_rateFood()
    test_getFloodSizeList()
    test_avoidHeadMoves()
