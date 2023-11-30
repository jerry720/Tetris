from tkinter import *
from constants import GAME_SPEED, BG_COLOUR, BD_WIDTH


class Tile:

    def __init__(self, name):
        self.name = name
        self.colour = None
        self.pivot = (2, 4) # pivot for rotation
        self.brick_num = 4
        self.speed = 2
        self.shape = {} # A 3D array to hold different positions of shape
        self.current = 0 # default shape position
        
    def create_shape(self, grid, x, y): # grid is a 2D list of button objects; x, y is position of pivot
        #print('Pivot:', self.get_pivot())
        grid[x][y].configure(bg=self.colour)
        for i, j in self.shape.get(self.current):
            grid[x+i][y+j].configure(bg=self.colour)        

    def erase_shape(self, grid, x, y):
        grid[x][y].configure(bg=BG_COLOUR)
        for i, j in self.shape.get(self.current):
             grid[x+i][y+j].configure(bg=BG_COLOUR)

    def rotate_profile(self): # rotate shape profile clockwise
        current_duplicate = self.current + 1 # duplicates current profile
        if current_duplicate > max(self.shape.keys()):
            current_duplicate = 0
        return current_duplicate

    def rotate(self, grid): # actually rotating the shape
        self.current = self.rotate_profile()
        self.create_shape(grid, *self.pivot)
        
    def set_pivot(self, x, y):
        self.pivot = (x, y)

    def get_pivot(self):
        return self.pivot

    def get_current_shape(self, x, y): # including pivot
        original = list(map(lambda z: (z[0]+x, z[1]+y), [movement for movement in self.shape.get(self.current)]))
        original.append((x, y))
        return original

    def get_not_overlapping(self, coords_1: list, coords_2: list): # list of tuples
        '''Note coords_1 should always be the current coordinates'''
        coords_1 = set(coords_1)
        coords_2 = set(coords_2)
        return list(coords_2 - coords_1) # returns non overlapping squares

    def check_collision(self, grid, x, y, direction):
        allowed_colours = [BG_COLOUR]
        status = self.shape.get(self.current)
        if direction == 'left':
            offset = (0, -1)
        elif direction == 'right':
            offset = (0, 1)
        elif direction == 'down':
            offset = (1, 0)
        elif direction == 'up':
            offset = (0, 0)
        else:
            raise ValueError('Inappropriate direction argument')
        # all squares occupied by the shape moved according to offset
        occupied = list(map(lambda z: (z[0]+x+offset[0], z[1]+y+offset[1]), [movement for movement in status]))
        occupied.append((x+offset[0], y+offset[1])) # adding pivot coordinates shifted down 1
        try: # catcing index errors
            # checking that non-overlapping future squares are same as bg_clr to allow movement
            if all([grid[square[0]][square[1]].cget('bg') in allowed_colours for square in self.get_not_overlapping(self.get_current_shape(x, y), occupied)]):
                if direction == 'left':
                    return all([square[1]>=0 for square in occupied])
                elif direction == 'right':
                    return all([square[1]<len(grid[0]) for square in occupied])
                elif direction == 'down':
                    return all([square[0]<len(grid) for square in occupied])
            else:
                return False
        except:
            return False

    def check_rotation_collision(self, grid, x, y):
        # 3 cases
        # can't rotate - False
        # can rotate - True
        # can rotate, but have to move after rotation - None
        allowed_colours = [BG_COLOUR]
        original_profile = self.get_current_shape(*self.pivot)
        new_profile = self.rotate_profile() # not altering the original profile
        status = self.shape.get(new_profile)
        # profile of rotated shape
        occupied = list(map(lambda z: (z[0]+x, z[1]+y), [movement for movement in status]))
        occupied.append((x, y))
        # rotated shape within grid boundaries
        if all([square[0]<len(grid) and square[1]>=0 and square[1]<len(grid[0]) for square in occupied]):
            # rotated shape not overlapping with other pieces
            if all([grid[square[0]][square[1]].cget('bg') in allowed_colours for square in self.get_not_overlapping(self.get_current_shape(x, y), occupied)]):
                return True
        else:
            # extra checks to see if rotation conditions are met when shifted
            moved_left = list(map(lambda z: (z[0], z[1]-1), occupied))
            moved_right = list(map(lambda z: (z[0], z[1]+1), occupied))

            if all([square[0]<len(grid) and square[1]>=0 and square[1]<len(grid[0]) for square in moved_left]):
                if all([grid[square[0]][square[1]].cget('bg') in allowed_colours for square in self.get_not_overlapping(original_profile, moved_left)]):
                    return 'left'
                else:
                    return False
            if all([square[0]<len(grid) and square[1]>=0 and square[1]<len(grid[0]) for square in moved_right]):
                if all([grid[square[0]][square[1]].cget('bg') in allowed_colours for square in self.get_not_overlapping(original_profile, moved_right)]):
                    return 'right'
                else:
                    return False
            return False

      
                
