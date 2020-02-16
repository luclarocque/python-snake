import random
from scipy import spatial
from coord_tools import *


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


def avoidEdges(data, edgeBuffer=1):
    """
    avoidEdges returns a set of moves whose distance to walls is >=edgeBuffer
    """
    w = data['board']['width']
    h = data['board']['height']

    goodMoves = set()
    for mv in ['up', 'down', 'left', 'right']:
        newHead = movedHead(data, mv)
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
    head = dictToTuple(data['you']['body'][0])
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


# TODO: iterate through goToPoint() with all foods in output of rateFood().
#  Assign weight based on inverse of cost (rating), and choose most strongly
#  weighted direction as next move.
def nextMove(data):
    """
    nextMove is the main function used to return a single move to the API.
    """
    # health = data['you']['health']
    possMoves = possibleMoves(data)
    print("possMoves", possMoves)

    foodList = [tup[0] for tup in rateFood(data)]
    foodMoves = set(possMoves)  # copy the set of possMoves
    # find a move that brings you closer to the nearest food
    print(foodList[:1])
    for point in foodList[:1]:
        foodMoves &= goToPoint(data, point)  # intersect sets: common moves
    print("moves toward nearest food", foodMoves)
    # otherwise find moves that will approach any food
    if not foodMoves:
        print("can't go towards nearest food")
        foodMoves = set()
        for point in foodList:
            foodMoves |= goToPoint(data, point)
    subsetMoves = foodMoves & possMoves
    print("possible foodMoves", subsetMoves)
    # else:
    #     subsetMoves = avoidEdges(data, possMoves, edgeBuffer=2)
    if not subsetMoves:
        subsetMoves = possMoves
    move = random.choice(list(subsetMoves))
    print("final moveSet", subsetMoves)
    return move
