def getWidthHeight(data):
    w = data['board']['width']
    h = data['board']['height']
    return w, h


def getHead(data):
    return dictToTuple(data['you']['body'][0])


def movePoint(point, moveDirection):
    """
    movePoint returns a tuple (x,y) of the point after moving in moveDirection
    """
    x, y = ensurePoint(point)
    switchPoint = {
        'up': (x, y - 1),
        'down': (x, y + 1),
        'left': (x - 1, y),
        'right': (x + 1, y)
    }
    return switchPoint[moveDirection]


def distance(a, b):
    """
    distance computes the Manhattan distance between a and b
        where a and b are either tuples (x,y) or dicts {'x':_, 'y':_}
    """
    if not isinstance(a, tuple):
        a = (a['x'], a['y'])
    if not isinstance(b, tuple):
        b = (b['x'], b['y'])
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def dictToTuple(d):
    return d['x'], d['y']


def listDictToTuple(listDicts):
    return [dictToTuple(d) for d in listDicts]


def ensurePoint(d):
    if not isinstance(d, tuple):
        d = dictToTuple(d)
    return d


def withinBoard(point, w, h):
    x, y = ensurePoint(point)
    return 0 <= x < w and 0 <= y < h


def distHeadToWalls(head, w, h):
    """
    distHeadToWalls returns a dict
        {key=direction : val=distance to wall in that direction}
    head can be either getHead(data)   OR   a tuple (x,y)
    w, h are the board width and board height, respectively
    """
    x, y = ensurePoint(head)
    switchDistance = dict(up=y, down=(h - 1) - y, left=x, right=(w - 1) - x)
    return switchDistance


def goToPoint(data, point):
    """
    goToPoint returns a set of moves that decrease the distance to the point
    """
    head = getHead(data)
    moves = set()
    if point[0] > head[0]:
        moves |= {'right'}
    elif point[0] < head[0]:
        moves |= {'left'}
    if point[1] > head[1]:
        moves |= {'down'}
    elif point[1] < head[1]:
        moves |= {'up'}
    return moves

# TODO: visualize board given json data
