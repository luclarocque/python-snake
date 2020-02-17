import random
from scipy import spatial
from coord_tools import *


# TODO: check args of hitWall, hitSnake,

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


def rateFood(data):
    """
    rateFood returns None (no food) or a list of tuples ((x, y), cost)
        where (x,y) are the coords of the food, and
        cost is determined by distance (and other metrics???)
    Note: lower rating => better
    """
    # TODO: add more to cost, e.g., is it central? is it in a large zone?
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
    ratings = [(listFood[indices[i]], distances[i]) for i in range(len(distances))]
    print(ratings)
    return ratings


def goToFood(data, k=3):
    foodList = [tup[0] for tup in rateFood(data)]
    # find moves that brings you closer to the nearest food
    foodMoves = set()
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

    # accumulate coords in dictPoints
    def floodHelper(data, point, dictPoints):
        if not withinBoard(point, w, h):  # base case: point outside board
            return dictPoints
        elif dictPoints.get(point, False):  # base case: already visited
            return dictPoints
        elif data['snakeMap'].get(point, False):  # base case: point in snake
            return dictPoints
        dictPoints[point] = True
        if not hitAny(data, point, 'up'):
            floodHelper(data, movePoint(data, 'up'), dictPoints)
        if not hitAny(data, point, 'down'):
            floodHelper(data, movePoint(data, 'down'), dictPoints)
        if not hitAny(data, point, 'left'):
            floodHelper(data, movePoint(data, 'left'), dictPoints)
        if not hitAny(data, point, 'right'):
            floodHelper(data, movePoint(data, 'right'), dictPoints)

    return floodHelper(data, point, {})



def floodZones(data):
    head = getHead(data)
    w, h = getWidthHeight(data)

    # def floodZonesHelper(data, point, zoneMap):
    #     if not withinBoard(point, w, h):  # base case: point outside board
    #         return zoneMap
    #     if data['snakeMap'].get(point, False):  # base case: point in snake
    #         return zoneMap
    #
    #     return floodZonesHelper()


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
    # ------------------------------------------------------------------------|

    health = data['you']['health']
    possMoves = possibleMoves(data)
    print("possMoves", possMoves)

    if health < 80:
        subsetMoves = goToFood(data)
    else:
        subsetMoves = avoidEdges(data, edgeBuffer=2)
    subsetMoves &= possMoves
    if not subsetMoves:
        subsetMoves = possMoves
    move = random.choice(list(subsetMoves))
    print("final moveSet", subsetMoves)
    return move
