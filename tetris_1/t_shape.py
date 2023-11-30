from tile import Tile

class TShape(Tile):
    '''
     #
    ###
    '''
    def __init__(self, name='t'):
        super().__init__(name)
        self.colour = '#71ebe0'
        self.preview_center = (2, 1)
        self.shape = {
            0: [(-1, 0), (0, -1), (0, 1)],
            1: [(-1, 0), (0, 1), (1, 0)],
            2: [(0, -1), (0, 1), (1, 0)],
            3: [(-1, 0), (0, -1), (1, 0)]
            } 

