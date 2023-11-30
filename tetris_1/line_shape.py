from tile import Tile


class LineShape(Tile):
    '''
    #
    #
    #
    #
    '''

    def __init__(self, name='line'):
        super().__init__(name) # inheriting attributes from the constructor of superclass
        self.colour = '#37a4db'
        self.preview_center = (1, 1) # center for preview allignment
        # representation of the shape around a pivot (rotating clockwise)
        self.shape = {
            0: [(0, -1), (0, 1), (0, 2)],
            1: [(-1, 0), (-2, 0), (1, 0)],
            2: [(0, -2), (0, -1), (0, 1)],
            3: [(-1, 0), (1, 0), (2, 0)]
            }        
        
