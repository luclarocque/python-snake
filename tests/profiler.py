import cProfile
from testing_tools import resetData
from app.snake_helpers import *

data = resetData(8)
cProfile.run('nextMove(data)')
