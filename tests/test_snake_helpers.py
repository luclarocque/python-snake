import json
from app.snake_helpers import *

def resetData():
    with open('../examples/request_example1.json') as jsonData:
        data = json.load(jsonData)
    return data

def redefineYou(data, listPoints):
    ''' redefineYou modifies data in-place
    listPoints: first elem is head, must be in order
    '''
    data['you']['body'] = []
    for pt in listPoints:
        coords = {'x': pt[0], 'y': pt[1]}
        data['you']['body'].append(coords)
    data['board']['snakes'][0] = data['you']
    print(data)

newSnakeCount = 0
def addSnake(data, listPoints):
    newSnakeCount += 1
    newSnake = {
        'id': str(newSnakeCount),
        'name': 'Snek'+str(newSnakeCount),
        'health': 90,
        'body': []
    }
    for pt in listPoints:
        coords = {'x': pt[0], 'y': pt[1]}
        newSnake['body'].append(coords)
    # add the new snake to snakes (list)
    data['board']['snakes'].append(newSnake)



def test_willCollide(data):
    print("should not collide with wall, going up")
    assert willCollide(data, 'up') is False

    print("should collide with wall, going left")
    redefineYou(data, [(0,3)])
    assert willCollide(data, 'left') is True


if __name__ == "__main__":
    data = resetData()
    test_willCollide(data)
