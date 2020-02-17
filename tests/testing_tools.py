import json
from app.snake_helpers import nextMove


def resetData(exampleNum):
    def switchFile(fileNumber):
        switch = {
            1: '../examples/example_only_you.json',
            2: '../examples/example_two_snakes.json',
            3: '../examples/example_facing_wall.json'
        }
        return switch[fileNumber]

    jsonFile = switchFile(exampleNum)
    with open(jsonFile) as jsonData:
        data = json.load(jsonData)
    nextMove(data)  # call this here since it initializes some keys in data
    return data

# DEPRECATED???
# def redefineYou(data, listPoints):
#     """
#     redefineYou modifies data in-place
#     listPoints: list of tuples (x,y); first elem is head, must be in order
#     """
#     data['you']['body'] = []
#     for pt in listPoints:
#         coords = {'x': pt[0], 'y': pt[1]}
#         data['you']['body'].append(coords)
#     data['board']['snakes'][0] = data['you']


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