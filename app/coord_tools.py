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


def distHeadToWalls(head, w, h):
    """
    distHeadToWalls returns a dict
        {key=direction : val=distance to wall in that direction}
    head can be either data['you']['body'][0]   OR   a tuple (x,y)
    w, h are the board width and board height, respectively
    """
    # get x and y coords of head
    if isinstance(head, tuple):
        x = head[0]
        y = head[1]
    else:
        x = head['x']
        y = head['y']

    switchDistance = dict(up=y, down=(h - 1) - y, left=x, right=(w - 1) - x)
    return switchDistance


def goToPoint(data, point):
    """
    goToPoint returns a set of moves that decreases the distance to the point
    """
    head = dictToTuple(data['you']['body'][0])
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
