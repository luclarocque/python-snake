import random
from scipy import spatial
from coord_tools import *

directions = ('up', 'down', 'left', 'right')


def mapSnakes(data):
    snakeBodyPoints = {}
    for snake in data['board']['snakes']:
        for snakePoint in snake['body'][0:-1]:  # do not worry about hitting tail
            snakeBodyPoints[(snakePoint['x'], snakePoint['y'])] = True
    return snakeBodyPoints


def hitWall(data, point, moveDirection):
    w, h = getWidthHeight(data)
    point = movePoint(point, moveDirection)
    return not withinBoard(point, w, h)


# Check for collision with another snake (minus tails)
def hitSnake(data, point, moveDirection):
    point = movePoint(point, moveDirection)
    return data['snakeMap'].get(point, False)  # defaults to False if not found


def hitAny(data, point, moveDirection):
    return hitWall(data, point, moveDirection) or hitSnake(data, point, moveDirection)


# TODO: this assumes other snake does not move. Must look one step ahead for possible collision.
# Assuming hitSnake, check if head-on collision AND if you are longer
# def headOnWin(data, moveDirection):
#     snakeHeads = {}  # key=(x,y) of head : value=len(snake)
#     for snake in data['board']['snakes']:
#         if snake['id'] == data['you']['id']:
#             continue  # skip adding your own head
#         x, y = getHead(data)
#         snakeHeads[(x, y)] = len(snake)
#     head = getHead(data)
#     newHead = movePoint(head, moveDirection)
#
#     # check if your head will collide with another head, and if you survive
#     opponentLen = snakeHeads.get(newHead, 0)
#     yourLen = len(data['you']['body'])
#     return yourLen > opponentLen


def possibleMoves(data):
    moves = {'up', 'down', 'left', 'right'}
    head = getHead(data)
    goodMoves = set()
    for mv in moves:
        if not hitAny(data, head, mv):
            goodMoves |= {mv}
    return goodMoves


def avoidEdges(data, edgeBuffer=1):
    """
    avoidEdges returns a set of moves whose distance to walls is >=edgeBuffer
    """
    w, h = getWidthHeight(data)
    goodMoves = set()
    for mv in ['up', 'down', 'left', 'right']:
        head = getHead(data)
        newHead = movePoint(head, mv)
        switchDistance = distHeadToWalls(newHead, w, h)
        dist = switchDistance[mv]
        if dist >= edgeBuffer:
            goodMoves |= {mv}
    return goodMoves


def getFoodDistList(data):
    """
    getFoodDistList returns None (no food) or a list of tuples ((x, y), dist)
        where (x,y) are the coords of the food, and dist is distance
    Note: lower rating => better
    """
    head = getHead(data)
    listFood = listDictToTuple(data['board']['food'])
    if not listFood:
        return None
    tree = spatial.KDTree(listFood)
    distances, indices = tree.query(head, k=len(listFood), p=1)
    if isinstance(distances, float):  # kdtree.query returns float if only 1 food
        distances = [distances]
        indices = [indices]
    distances = map(int, distances)
    foodDistList = [(listFood[indices[i]], distances[i]) for i in range(len(distances))]
    print(foodDistList)
    return foodDistList


def goToFood(data, k=3):
    """
    goToFood returns a set of moves that bring you closer to either
        the nearest food to your head, or one of k nearest foods.
    """
    foodDistList = getFoodDistList(data)
    foodMoves = set()
    if not foodDistList:
        return foodMoves
    foodList = [tup[0] for tup in foodDistList]  # list of food coords
    # find moves that brings you closer to the nearest food
    for point in foodList[:1]:
        foodMoves |= goToPoint(data, point)
    # otherwise find moves that will approach any of nearest k foods
    if not foodMoves:
        print("can't go towards nearest food")
        foodMoves = set()
        for point in foodList[:k]:
            foodMoves |= goToPoint(data, point)
    return foodMoves


def flood(data, point):
    w, h = getWidthHeight(data)

    # accumulate coords of empty spaces(+tails) in dictPoints
    dictPoints = {}

    def floodHelper(curPoint):
        if not withinBoard(curPoint, w, h):  # base case: wall / outside board
            return
        elif dictPoints.get(curPoint, False):  # base case: already visited
            return
        elif data['snakeMap'].get(curPoint, False):  # base case: point in snake
            return

        dictPoints[curPoint] = True  # otherwise add current point to flood set
        for d in directions:
            floodHelper(movePoint(curPoint, d))

    floodHelper(point)  # run once to populate dictPoints
    return dictPoints


def getFloodSizeList(data):
    """
    getFloodSizeList returns a list of tuples (move, size)
        where move is a direction (str),
        size is the flood size if the head were to move in that direction
    Note: flooding always happens from the perspective of the head
    """
    head = getHead(data)
    floodSizeList = []
    for d in directions:
        floodSet = flood(data, movePoint(head, d))
        floodSizeList.append((d, len(floodSet)))
    # sort in order of descending flood size
    return sorted(floodSizeList, key=lambda x: x[1], reverse=True)


# TODO: create dictionary of possible moves {key='move': val=rating}
#   increase score for moving toward food, avoiding edges, staying in
#   large zones, etc.
def rateMoves(data, possMoves):
    pass


def nextMove(data):
    """
    nextMove is the main function used to return a single move to the API.
    """
    # INITIALIZE NEW DATA KEYS HERE ------------------------------------------|
    data['snakeMap'] = mapSnakes(data)
    data['floodSizeList'] = getFloodSizeList(data)
    data['foodDistList'] = getFoodDistList(data)
    # ------------------------------------------------------------------------|

    health = data['you']['health']
    myLength = len(data['you']['body'])

    possMoves = possibleMoves(data)
    print("possMoves", possMoves)

    # set of moves that bring you closer to food
    foodMoves = goToFood(data)
    print("foodMoves", foodMoves)

    # set of moves that lead to open space, in descending order
    highFloodMoves = list(map(lambda y: y[0],  # the move is at index 0
                              filter(lambda x: x[1] > 0, data['floodSizeList'])))
    print("highFloodMoves", highFloodMoves)

    # Moves in highFloodMoves must be possible
    #   Choose the first move that leads to food as well
    for mv in highFloodMoves:
        if mv in foodMoves:
            return mv

    # If no highFloodMoves head toward food, go in highest flood direction
    return highFloodMoves[0]
