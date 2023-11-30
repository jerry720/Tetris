from tile import Tile

class ZShapeLeft(Tile):
    '''
     #
    ##
    #
    '''
    def __init__(self, name='z_left'):
        super().__init__(name)
        self.colour = '#bae305'
        self.preview_center = (1, 1)
        self.shape = {
            0: [(0, 1), (-1, 1), (1, 0)],
            1: [(0, -1), (1, 0), (1, 1)]
            } 
