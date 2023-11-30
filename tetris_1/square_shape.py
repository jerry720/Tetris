from tile import Tile

class SquareShape(Tile):
    '''
    ##
    ##
    '''
    def __init__(self, name='square'):
        super().__init__(name)
        self.colour = '#eb4438'
        self.preview_center = (2, 1)
        self.shape = {
            0: [(-1, 0), (0, 1), (-1, 1)]
            }

