import json
from app.snake_helpers import *


def resetData(exampleNum):
    def switchFile(fileNumber):
        switch = {
            1: '../examples/example_only_you.json',
            2: '../examples/example_two_snakes.json'
        }
        return switch[fileNumber]

    jsonFile = switchFile(exampleNum)
    with open(jsonFile) as jsonData:
        data = json.load(jsonData)
    return data


def redefineYou(data, listPoints):
    """
    redefineYou modifies data in-place
    listPoints: list of tuples (x,y); first elem is head, must be in order
    """
    data['you']['body'] = []
    for pt in listPoints:
        coords = {'x': pt[0], 'y': pt[1]}
        data['you']['body'].append(coords)
    data['board']['snakes'][0] = data['you']


newSnakeCount = 0


def addSnake(data, listPoints):
    global newSnakeCount
    newSnakeCount += 1
    newSnake = {
        'id': str(newSnakeCount),
        'name': 'Snek' + str(newSnakeCount),
        'health': 90,
        'body': []
    }
    for pt in listPoints:
        coords = {'x': pt[0], 'y': pt[1]}
        newSnake['body'].append(coords)
    # add the new snake to snakes (list)
    data['board']['snakes'].append(newSnake)


def test_hitWall():
    data = resetData(1)

    print("should collide with wall, going up")
    redefineYou(data, [(6, 0)])
    assert hitWall(data, 'up') is True

    print("should collide with wall, going left")
    redefineYou(data, [(0, 3)])
    assert hitWall(data, 'left') is True

    print("should collide with wall, going right")
    redefineYou(data, [(data['board']['width'], 3)])
    assert hitWall(data, 'right') is True

    print("should collide with wall, going down")
    redefineYou(data, [(6, data['board']['height'])])
    assert hitWall(data, 'down') is True

    print("should not collide with wall, going up")
    redefineYou(data, [(6, data['board']['height'])])
    assert hitWall(data, 'up') is False


def test_hitSnake():
    data = resetData(2)

    print("should not collide with snake, going right (tail)")
    assert hitSnake(data, 'right') is False

    print("should collide with snake, going up")
    assert hitSnake(data, 'up') is True

    print("should collide with SELF, going down")
    assert hitSnake(data, 'down') is True

    print("should not collide with snake, going left (although off board)")
    assert hitSnake(data, 'left') is False


def test_possibleMoves():
    data = resetData(1)
    print("should be able to move any direction")
    assert possibleMoves(data) == {'up', 'down', 'left', 'right'}

    data = resetData(2)
    print("should be able to move left or right (tail is right)")
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
    print("should avoid being next to wall (do not allow left)")
    possible = possibleMoves(data)
    assert avoidEdges(data, possible, 1) == {'up', 'down', 'right'}


if __name__ == "__main__":
    test_hitWall()
    test_hitSnake()
    test_possibleMoves()
    test_distHeadToWalls()
    test_avoidEdges()
