import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from app.coord_tools import *
from testing_tools import resetData


def visualize(data):
    colours = ['pink', 'red', 'blue', 'green', 'black', 'cyan', 'purple', 'yellow']

    w, h = getWidthHeight(data)
    me = data['you']['body']
    snakes = data['board']['snakes']

    fig, ax = plt.subplots()

    for snake in snakes:
        coords = map(lambda p: (p[0] + 0.5, p[1] + 0.5), listDictToTuple(snake['body']))
        if snake['death'] == "null":
            continue
        elif snake['name'].lower() == "lucwashere / slython":
            plt.scatter(*zip(*coords), c='pink', s=1050, marker='s')
        else:
            plt.scatter(*zip(*coords), s=900, marker='s')
        plt.scatter(*coords[0], c='k', s=400, marker='*')

    # TODO: fix grid spacing to make perfect squares
    # draw gridlines
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(0, w))
    ax.set_yticks(np.arange(0, h))
    ax.set_xlim([0, w])
    ax.set_xlim([0, h])
    plt.gca().invert_yaxis()

    plt.show()


if __name__ == "__main__":
    data = resetData(7)
    visualize(data)