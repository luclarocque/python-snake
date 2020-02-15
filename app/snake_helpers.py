import random


def movedHead(data, moveDirection):
    '''
    movedHead returns a tuple (x,y) of the head after moving in moveDirection
    '''
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
def headOnWin(data, moveDirection):
    snakeHeads = {}  # key=(x,y) of head : value=len(snake)
    for snake in data['board']['snakes']:
        head = snake['body'][0]  # includes your own head, but movedHead is always different
        snakeHeads[(head['x'], head['y'])] = len(snake)

    newHead = movedHead(data, moveDirection)

    # check if your head will collide with another head, and if you survive
    opponentLen = snakeHeads.get(newHead, 0)
    yourLen = len(data['you']['body'])
    return yourLen > opponentLen


def possibleMoves(data):
    directions = ['up', 'down', 'left', 'right']
    possible = []
    for d in directions:
        if not(hitAny(data, d)):
            possible.append(d)
    return possible


def nextMove(data):
    directions = possibleMoves(data)
    direction = random.choice(directions)
    return direction
