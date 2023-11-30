from tile import Tile

class ZShapeRight(Tile):
    '''
    #
    ##
     #
    '''
    def __init__(self, name='z_right'):
        super().__init__(name)
        self.colour = '#818185'
        self.preview_center = (1, 2)
        self.shape = {
            0: [(-1, -1), (0, -1), (1, 0)],
            1: [(-1, 0), (-1, 1), (0, -1)]
            }
