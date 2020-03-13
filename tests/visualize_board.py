import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from app.coord_tools import *
from testing_tools import resetData, snakeIsMe


def visualize(data):
    w, h = getWidthHeight(data)

    fig, ax = plt.subplots()

    # plot snakes
    for snake in data['board']['snakes']:
        coords = list(map(lambda p: (p[0] + 0.5, p[1] + 0.5), listDictToTuple(snake['body'])))
        if snake.get('death', None) is None:
            if snakeIsMe(snake):
                plt.scatter(*zip(*coords), c='pink', s=700, marker='s')
            else:
                plt.scatter(*zip(*coords), s=700, marker='s')
            plt.scatter(*coords[0], c='k', s=350, marker='*')

    # plot food
    food = data['board']['food']
    coords = list(map(lambda p: (p[0] + 0.5, p[1] + 0.5), listDictToTuple(food)))
    plt.scatter(*zip(*coords), c='m', s=250, marker='o')

    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(0, w))
    ax.set_yticks(np.arange(0, h))
    plt.xlim(0, w)
    plt.ylim(0, h)
    plt.gca().invert_yaxis()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


if __name__ == "__main__":
    data = resetData(8)
    visualize(data)