import json
import os
import bottle
from snake_helpers import nextMove

from api import ping_response, start_response, move_response, end_response


@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.com">https://docs.battlesnake.com</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


games = {}


@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print "\n", "*-"*5, 'START GAME', "-*"*5, "\n"
    print(json.dumps(data))

    games[data['game']['id']] = data
    color = "#FC3EC5"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json
    games[data['game']['id']] = data

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """

    direction = nextMove(data)

    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print('\n*------END------*')
    print(json.dumps(data))
    games.pop(data['game']['id'])

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
