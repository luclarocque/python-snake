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


def getFoodMoves(data, k=3):
    """
    getFoodMoves returns a set of moves that bring you closer to either
        the nearest food to your head, or one of k nearest foods.
    NOTE: Only returns moves that do not result in direct collision
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
        # foodMoves = set()
        for point in foodList[1:k]:
            foodMoves |= goToPoint(data, point)
    possMoves = possibleMoves(data)
    return foodMoves & possMoves


def flood(data, point, snakeMap):
    """
    flood returns a dictionary of vacant coords (incl. tails) in the zone
        that includes the given input point.
    """
    w, h = getWidthHeight(data)

    # accumulate coords of empty spaces(+tails) in dictPoints
    dictPoints = {}

    def floodHelper(curPoint):
        if not withinBoard(curPoint, w, h):  # base case: wall / outside board
            return
        elif dictPoints.get(curPoint, False):  # base case: already visited
            return
        elif snakeMap.get(curPoint, False):  # base case: point in snake
            return

        dictPoints[curPoint] = True  # otherwise add current point to flood set
        for d in directions:
            floodHelper(movePoint(curPoint, d))

    floodHelper(point)  # run once to populate dictPoints
    return dictPoints


def getFloodSizeList(data, snakeMap):
    """
    getFloodSizeList returns a list of tuples (move, size)
        where move is a direction (str),
        size is the flood size if the head were to move in that direction
    Note: flooding always happens from the perspective of the head
    """
    head = getHead(data)
    floodSizeList = []
    for d in directions:
        floodSet = flood(data, movePoint(head, d), snakeMap)
        floodSizeList.append((d, len(floodSet)))
    # sort in order of descending flood size
    return sorted(floodSizeList, key=lambda x: x[1], reverse=True)


def getHeadMap(data):
    """
    getHeadMap returns a dict:
        key=(x,y) of opponent snakeHeads : value=len(snake)
    """
    snakeHeads = {}  # key=(x,y) of head : value=len(snake)
    for snake in data['board']['snakes']:
        if snake['id'] == data['you']['id']:
            continue  # skip adding your own head
        opponentHead = snake['body'][0]
        for d in directions:
            possibleHead = movePoint(opponentHead, d)
            snakeHeads[possibleHead] = len(snake)
    return snakeHeads


# TODO: perhaps return max 2 possible moves if we can kill a smaller snake
def avoidHeadMoves(data, headMap):
    """
    avoidHeadMoves returns set of moves that cannot result in losing
        head-on collision.
    NOTE: Only returns moves that do not result in direct collision
    """
    myLength = len(data['you']['body'])
    head = getHead(data)

    moves = set()
    for d in directions:
        movedHead = movePoint(head, d)
        opponentLength = headMap.get(movedHead, False)
        if not opponentLength or myLength > opponentLength:
            moves |= {d}
    possMoves = possibleMoves(data)
    return moves & possMoves


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
    data['floodSizeList'] = getFloodSizeList(data, data['snakeMap'])
    data['foodDistList'] = getFoodDistList(data)
    data['headMap'] = getHeadMap(data)
    # ------------------------------------------------------------------------|

    health = data['you']['health']
    myLength = len(data['you']['body'])

    # set of moves that bring you closer to food
    foodMoves = getFoodMoves(data)
    print("foodMoves", foodMoves)

    # set of moves that avoid heads of larger snakes
    # TODO: actively target heads of smaller snakes?
    headMoves = avoidHeadMoves(data, data['headMap'])
    print("headMoves", headMoves)

    # list of (move, size) that lead to open space, in descending order
    highFloodMovesSizes = list(filter(lambda x: x[1] > 0, data['floodSizeList']))
    print("highFloodMovesSizes", highFloodMovesSizes)

    # list of moves only from highFloodMovesSizes
    highFloodMoves = [tup[0] for tup in highFloodMovesSizes]
    print("highFloodMoves", highFloodMoves)

    # Moves in highFloodMovesSizes must be possible
    #   Choose the first move that leads to food as well
    # for mv, size in highFloodMovesSizes:
    #     if mv in foodMoves and size > myLength/2:
    #         return mv

    # TODO: must find a way to balance priorities.
    #   - Food is lowest priority, but increases (exponentially?) with decreasing health
    #   - headMoves is high priority, but it is conservative: moves not in this set are not
    #       guaranteed to result in death, but death is not unlikely
    #   - highFloodMovesSizes with large size are high priority
    for mv, size in highFloodMovesSizes:
        if mv in headMoves:
            if mv in foodMoves and size > myLength/2:
                return mv

    # If chasing food is not possible settle for avoiding heads in large zones
    if highFloodMoves[0] in headMoves:
        return highFloodMoves[0]
    elif highFloodMovesSizes[1][1] > myLength/2 and highFloodMoves[1] in headMoves:
        return highFloodMoves[1]
    else:
        return highFloodMoves[0]
