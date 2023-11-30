from tile import Tile

class LShapeRight(Tile):
    '''
     #
     #
     ##
    '''
    def __init__(self, name='l_right'):
        super().__init__(name)
        self.colour = '#c964f5'
        self.preview_center = (1, 1)
        self.shape = {
            0: [(-1, 0), (1, 0), (1, 1)],
            1: [(1, -1), (0, -1), (0, 1)],
            2: [(-1, 0), (1, 0), (-1, -1)],
            3: [(0, -1), (0, 1), (-1, 1)]
            } 
