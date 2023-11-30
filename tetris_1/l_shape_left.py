from tile import Tile

class LShapeLeft(Tile):
    '''
     #
     #
    ##
    '''
    def __init__(self, name='l_left'):
        super().__init__(name)
        self.colour = '#f7972f'
        self.preview_center = (1, 2)
        self.shape = {
            0: [(-1, 0), (1, 0), (1, -1)],
            1: [(-1, -1), (0, -1), (0, 1)],
            2: [(-1, 0), (1, 0), (-1, 1)],
            3: [(0, -1), (0, 1), (1, 1)]
            } 

