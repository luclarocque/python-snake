import random
from scipy import spatial
from coord_tools import *


def movedHead(data, moveDirection):
    """
    movedHead returns a tuple (x,y) of the head after moving in moveDirection
    """
    head = data['you']['body'][0]
    switchHead = {
        'up': (head['x'], head['y'] - 1),
        'down': (head['x'], head['y'] + 1),
        'left': (head['x'] - 1, head['y']),
        'right': (head['x'] + 1, head['y'])
    }
    return switchHead[moveDirection]


def hitWall(data, moveDirection):
    w = data['board']['width']
    h = data['board']['height']

    newHead = movedHead(data, moveDirection)
    x = newHead[0]
    y = newHead[1]
    return not(0 <= x < w and 0 <= y < h)


# Check for collision with another snake (minus tails)
def hitSnake(data, moveDirection):
    snakeBodyPoints = {}
    for snake in data['board']['snakes']:
        for snakePoint in snake['body'][0:-1]:  # do not worry about hitting tail
            snakeBodyPoints[(snakePoint['x'], snakePoint['y'])] = True

    # check if the movedHead is in already in snakeBodyPoints (collision)
    newHead = movedHead(data, moveDirection)
    return snakeBodyPoints.get(newHead, False)  # defaults to False if not found


def hitAny(data, moveDirection):
    return hitWall(data, moveDirection) or hitSnake(data, moveDirection)


# TODO: this assumes other snake does not move. Must look one step ahead for possible collision.
# Assuming hitSnake, check if head-on collision AND if you are longer
# def headOnWin(data, moveDirection):
#     snakeHeads = {}  # key=(x,y) of head : value=len(snake)
#     for snake in data['board']['snakes']:
#         head = snake['body'][0]  # includes your own head, but movedHead is always different
#         snakeHeads[(head['x'], head['y'])] = len(snake)
#
#     newHead = movedHead(data, moveDirection)
#
#     # check if your head will collide with another head, and if you survive
#     opponentLen = snakeHeads.get(newHead, 0)
#     yourLen = len(data['you']['body'])
#     return yourLen > opponentLen


def possibleMoves(data):
    moves = {'up', 'down', 'left', 'right'}
    goodMoves = set()
    for mv in moves:
        if not hitAny(data, mv):
            goodMoves |= {mv}
    return goodMoves


def avoidEdges(data, setMoves, edgeBuffer=1):
    """
    avoidEdges takes setMoves, a set of possible moves, and returns
        a subset of moves whose distance to walls is >=edgeBuffer.
    """
    w = data['board']['width']
    h = data['board']['height']

    goodMoves = set()
    for mv in setMoves:
        newHead = movedHead(data, mv)
        switchDistance = distHeadToWalls(newHead, w, h)
        dist = switchDistance[mv]
        if dist >= edgeBuffer:
            goodMoves |= {mv}

    return goodMoves


def nearestFood1(data):
    head = data['you']['body'][0]
    listFood = data['board']['food']
    if not listFood:
        return None
    nearest = listFood[0]
    for food in listFood:
        if distance(head, food) < distance(head, nearest):
            nearest = food
    return nearest


def nearestFood(data):
    head = dictToTuple(data['you']['body'][0])
    listFood = listDictToTuple(data['board']['food'])
    tree = spatial.KDTree(listFood)
    print(tree.query(head))
    dist, indNearest = tree.query(head)
    return listFood[indNearest]


def nextMove(data):
    """
    nextMove is the main function used to return a single move to the API.
    """
    possMoves = possibleMoves(data)
    subsetMoves = avoidEdges(data, possMoves, edgeBuffer=3)
    if not subsetMoves:
        subsetMoves = possMoves
    move = random.choice(list(subsetMoves))
    return move
