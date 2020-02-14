import copy
import random


def willCollide(data, moveDirection):
    w = data['board']['width']
    h = data['board']['height']

    head = data['you']['body'][0]

    # check for wall collision
    def hitWall(arg, head):
        switcher = {
            'up': head['y'] - 1 < 0,
            'down': head['y'] + 1 >= h,
            'left': head['x'] - 1 < 0,
            'right': head['x'] + 1 >= w
        }
        return switcher[arg]

    # Check for collision with another snake (minus tails)
    snakePoints = {}
    for snake in data['board']['snakes']:
        for snakePoint in snake['body'][0:-1]:
            snakePoints['{},{}'.format(snakePoint['x'], snakePoint['y'])] = True

    def hitSnake(arg, head):
        headMoved = {
            'up': '{},{}'.format(head['x'], head['y'] - 1),
            'down': '{},{}'.format(head['x'], head['y'] + 1),
            'left': '{},{}'.format(head['x'] - 1, head['y']),
            'right': '{},{}'.format(head['x'] + 1, head['y'])
        }
        return headMoved[moveDirection] in snakePoints

    return hitWall(moveDirection, head) or hitSnake(moveDirection, head)


def nextMove(data):
    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)
    return direction
