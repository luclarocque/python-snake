import json
import os
from app.snake_helpers import nextMove


def resetData(exampleNum):
    def switchFile(fileNumber):
        switch = {
            1: '../examples/example_only_you.json',
            2: '../examples/example_two_snakes.json',
            3: '../examples/example_facing_wall.json',
            4: '../examples/example_3_zones.json',
            5: '../examples/example_avoid_head.json',
            6: '../examples/example_food_head_priority_proper.json',
            7: '../examples/example_goright_avoid_equal_head_proper.json',
            8: '../examples/example_avoid_head_down_proper.json'
        }
        return switch[fileNumber]

    jsonFile = switchFile(exampleNum)
    with open(jsonFile) as jsonData:
        data = json.load(jsonData)
    nextMove(data)  # call this here since it initializes some keys in data
    return data


def lowerDict(dic):
    """
    lowerDict mutates dic recursively so that all keys that are strings are lowercase.
    """
    for k, v in dic.items():
        if isinstance(k, str) or isinstance(k, unicode):
            dic[k.lower()] = v
            dic.pop(k)
        if isinstance(v, dict):
            lowerDict(v)
        elif isinstance(v, list):
            for elem in v:
                lowerDict(elem)


def importExample(jsonFile, w=11, h=11):
    """
    importExample uses an example json file (saved in ../examples/) from Battlesnake WS
        to create a proper json data file
    """
    with open(jsonFile) as jsonData:
        boardData = json.load(jsonData)
        lowerDict(boardData)
        data = {u'game': {u'id': u'id123'}, u'board': boardData}
        data['board']['width'] = w
        data['board']['height'] = h
        for snake in data['board']['snakes']:
            if snake['name'] == "lucwashere / Slython":
                data['you'] = snake
    newFile = '..' + jsonFile.split('.')[-2] + '_proper.json'
    with open(newFile, 'w') as f:
        print("Creating " + newFile)
        json.dump(data, f)
        os.remove(jsonFile)  # delete old file
    return data


if __name__ == "__main__":
    importExample('../examples/example_avoid_head_down.json')
    pass
