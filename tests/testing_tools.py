import json
from app.snake_helpers import nextMove


def resetData(exampleNum):
    def switchFile(fileNumber):
        switch = {
            1: '../examples/example_only_you.json',
            2: '../examples/example_two_snakes.json',
            3: '../examples/example_facing_wall.json',
            4: '../examples/example_3_zones.json',
            5: '../examples/example_avoid_head.json'
        }
        return switch[fileNumber]

    jsonFile = switchFile(exampleNum)
    with open(jsonFile) as jsonData:
        data = json.load(jsonData)
    nextMove(data)  # call this here since it initializes some keys in data
    return data
