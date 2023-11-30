'''For package initialization, this file is
automatically executed when the tetris package is
imported. The use of this is to ensure that any
external program accessing this will have access to
all the necessary files it needs.'''

from constants import GAME_SPEED, BG_COLOUR, BD_WIDTH
from tile import Tile
from line_shape import LineShape
from square_shape import SquareShape
from t_shape import TShape
from l_shape_left import LShapeLeft
from l_shape_right import LShapeRight
from z_shape_left import ZShapeLeft
from z_shape_right import ZShapeRight
from game import Game
