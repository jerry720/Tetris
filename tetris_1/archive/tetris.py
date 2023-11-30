'''<tile> is generic and <block> is more specific'''


from tkinter import *
import random
import pprint


# constants
GAME_SPEED = 500# ms
BG_COLOUR = 'black'
BD_WIDTH = 1



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
        '''Note coords_1 should always be the corrent coordinates'''
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
        allowed_colours = [BG_COLOUR]
        new_profile = self.rotate_profile() # not altering the original profile
        status = self.shape.get(new_profile)
        occupied = list(map(lambda z: (z[0]+x, z[1]+y), [movement for movement in status]))
        occupied.append((x, y))
        try:
            if all([grid[square[0]][square[1]].cget('bg') in allowed_colours for square in self.get_not_overlapping(self.get_current_shape(x, y), occupied)]):
                return all([square[0]<len(grid) and square[1]>=0 and square[1]<len(grid[0]) for square in occupied])
            else:
                return False
        except:
            return False
                

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
        self.preview_center = (1, 2) # center for preview allignment
        # representation of the shape around a pivot (rotating clockwise)
        self.shape = {
            0: [(-1, 0), (-2, 0), (1, 0)],
            1: [(0, -1), (0, 1), (0, 2)],
            2: [(-1, 0), (1, 0), (2, 0)],
            3: [(0, -2), (0, -1), (0, 1)]
            }        
        

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


class Game:

    shapes = ('line', 'square', 't', 'l_left', 'l_right', 'z_left', 'z_right')
    shape_record = [] # to hold names of all instantiated objects
    
    def __init__(self, root):
##        super().__init__(master)
        self.root = root
        self.current_shape = Game.choose_shape()
        self.next_shape = Game.choose_shape()
        self.all_buttons = []
        self.event_handler = False # boolean flag to prevent rapid key-presses
        self.tetris_matrix = Frame(self.root)
        self.tetris_matrix.grid(row=1, column=0, rowspan=10, columnspan=18, padx=1, pady=3)
        self.running = False
        # creating a 2D grid
        for i in range(21):
            row = []
            for j in range(10):
                button = Button(self.tetris_matrix, text='', padx=12, pady=4, bg=BG_COLOUR, borderwidth=BD_WIDTH)
                if i > 2: # first 3 rows not displayed (spawning purposes)
                    button.grid(row=i, column=j)
                button.on = False # assigning custom attribute to button object
                row.append(button)
            self.all_buttons.append(row)
        self.setup_game()

    def up_key_press(self): # rotate shape
        if self.current_shape.check_rotation_collision(self.all_buttons, *self.current_shape.pivot):
            self.current_shape.erase_shape(self.all_buttons, self.current_shape.pivot[0], self.current_shape.pivot[1])
            self.current_shape.erase_shape(self.all_buttons, self.current_shape.pivot[0]-1, self.current_shape.pivot[1])
            self.current_shape.rotate(self.all_buttons)

    def left_key_press(self): # move shape left
        if not self.event_handler:
            if self.current_shape.check_collision(self.all_buttons, *self.current_shape.pivot, 'left'):
                self.event_handler = True
                self.current_shape.set_pivot(self.current_shape.pivot[0], self.current_shape.pivot[1]-1)
                self.current_shape.erase_shape(self.all_buttons, self.current_shape.pivot[0], self.current_shape.pivot[1])
                self.current_shape.erase_shape(self.all_buttons, self.current_shape.pivot[0], self.current_shape.pivot[1]+1)
                self.current_shape.create_shape(self.all_buttons, self.current_shape.pivot[0], self.current_shape.pivot[1])
                self.event_handler = False

    def right_key_press(self): # move shape right
        if not self.event_handler:
            if self.current_shape.check_collision(self.all_buttons, *self.current_shape.pivot, 'right'):  
                self.event_handler = True
                self.current_shape.set_pivot(self.current_shape.pivot[0], self.current_shape.pivot[1]+1)
                self.current_shape.erase_shape(self.all_buttons, self.current_shape.pivot[0], self.current_shape.pivot[1])
                self.current_shape.erase_shape(self.all_buttons, self.current_shape.pivot[0], self.current_shape.pivot[1]-1)
                self.current_shape.create_shape(self.all_buttons, self.current_shape.pivot[0], self.current_shape.pivot[1])
                self.event_handler = False

    def down_key_press(self): # move shape down
        if not self.event_handler:
            if self.current_shape.check_collision(self.all_buttons, *self.current_shape.pivot, 'down'):
                self.event_handler = True
                self.current_shape.set_pivot(self.current_shape.pivot[0]+1, self.current_shape.pivot[1])
                self.current_shape.erase_shape(self.all_buttons, self.current_shape.pivot[0], self.current_shape.pivot[1])
                self.current_shape.erase_shape(self.all_buttons, self.current_shape.pivot[0]-1, self.current_shape.pivot[1])
                self.current_shape.create_shape(self.all_buttons, self.current_shape.pivot[0], self.current_shape.pivot[1])
                self.event_handler = False

    def setup_game(self):
        self.root.title('Tetris')
        self.root.iconbitmap('tetris_block.ico')
        self.root.geometry('470x581')
        self.root.configure(bg='#171717')
        
        settings = LabelFrame(self.root, padx=0, pady=0)
        settings.grid(row=0, column=0)
        settings_button = Button(settings, text='⚙', padx=5, pady=5, borderwidth=0.7)
        settings_button.grid(row=0, column=0)
        self.game_type = Label(settings, text='Mode: Marathon', font=('Arial', 16, 'italic'))
        self.game_type.grid(row=0, column=1)
        
        
        preview_frame = LabelFrame(self.root, text='next')
        preview_frame.configure(bg='#3d3d3d')
        preview_frame.grid(row=3, column=25)
        self.preview = []
        for i in range(4):
            row = []
            for j in range(4):
                button = Button(preview_frame, padx=10, pady=3, bg=BG_COLOUR, borderwidth=BD_WIDTH)
                button.grid(row=i, column=j)
                row.append(button)
            self.preview.append(row)
        
        score_frame = LabelFrame(self.root, text='Score')
        score_frame.configure(bg='#3d3d3d')
        score_frame.grid(row=8, column=25)
        self.score = Label(score_frame, text='0', font=('Arial', 16, 'bold'))
        self.score.pack(padx=10, pady=10)
        self.event_log = Entry(score_frame, borderwidth=3, font=('Arial', 10))
        self.event_log.pack(padx=0, pady=0)


        # key - settings
        self.root.bind('<Up>',  lambda event: self.up_key_press())
        self.root.bind('<Left>',  lambda event: self.left_key_press())
        self.root.bind('<Right>',  lambda event: self.right_key_press())
        self.root.bind('<Down>', lambda event: self.down_key_press())
        self.root.bind('<Return>', lambda event: self.start_game())
        # next shape preview
        self.display_preview()

    def start_game(self):
        print('Game started')
        self.event_log.insert(0, 'Game started!')
        self.root.unbind('<Return>')
        self.running = True
        self.game_loop()

    def display_preview(self):
        for row in self.preview:
            for button in row:
                button.configure(bg=BG_COLOUR)
        center = self.next_shape.preview_center
        self.next_shape.get_current_shape(*center)
        self.next_shape.create_shape(self.preview, *center)
                
        

    # takes a list of tuples and switche light states to on
    def record_lights(self, coordinates: list):
        for x, y in coordinates:
            self.all_buttons[x][y].on = True

    def check_lights(self): # also increments score
        all_rows = []
        for i in range(3, len(self.all_buttons)):
            row = self.all_buttons[i] # a list of button objects
            if all([light.on for light in row]): # while row is filled
                all_rows.append(i)
        # incrementing score
        added_score = len(all_rows) * 10 * len(all_rows) # awarding multiple lines
        self.score.configure(text=str(int(self.score.cget('text'))+added_score))
        self.event_log.configure(foreground='black')
        if len(all_rows) == 2:
            msg = 'Double score!'
            self.event_log.configure(foreground='#faa02a')
            self.event_log.delete(0, END)
            self.event_log.insert(0, msg)
        elif len(all_rows) == 3:
            msg = 'Triple score!'
            self.event_log.configure(foreground='#faa02a')
            self.event_log.delete(0, END)
            self.event_log.insert(0, msg)
        elif len(all_rows) == 4:
            msg = 'Quadriple score!'
            self.event_log.configure(foreground='#faa02a')
            self.event_log.delete(0, END)
            self.event_log.insert(0, msg)
        return all_rows

    def delete_row(self, rows: list):
        for row in rows:
            # move all down by 1
            for i in range(row-1, 1, -1):
                for j in range(len(self.all_buttons[0])):
                    self.all_buttons[i+1][j].on = False
                    self.all_buttons[i+1][j].configure(bg=self.all_buttons[i][j].cget('bg'))
                    # changing light states
                    if not self.all_buttons[i+1][j].cget('bg') == BG_COLOUR:
                        self.all_buttons[i+1][j].on = True

    def check_lose(self):
        for button in self.all_buttons[1]:
            if button.on:
                return True
        return False

    @classmethod
    def record_shape(cls, obj):
        cls.shape_record.append(obj.name)

    @classmethod
    def choose_shape(cls): # returns an instantiated object
        shape = random.choice(cls.shapes)
        obj = None
        if shape == 'line':
            obj = LineShape()
        elif shape == 'square':
            obj = SquareShape()
        elif shape == 't':
            obj = TShape()
        elif shape == 'l_left':
            obj = LShapeLeft()
        elif shape == 'l_right':
            obj = LShapeRight()
        elif shape == 'z_left':
            obj = ZShapeLeft()
        elif shape == 'z_right':
            obj = ZShapeRight()
        return obj
            
    def game_loop(self): # creating a shape every time
        if self.running: # player hasn't lost
            '''List of tools
                - set_pivot of a shape to a new location
                - create_shape at a given pivot
                - erase_shape at a given pivot
                - check_collision for a shape
                
    '''
            # no imminent collision - continue
            if self.current_shape.check_collision(self.all_buttons, self.current_shape.pivot[0], self.current_shape.pivot[1], 'down'):
                self.current_shape.erase_shape(self.all_buttons, self.current_shape.pivot[0], self.current_shape.pivot[1])
                self.current_shape.set_pivot(self.current_shape.pivot[0]+1, self.current_shape.pivot[1])
                self.current_shape.create_shape(self.all_buttons, self.current_shape.pivot[0], self.current_shape.pivot[1])

            else:
                Game.record_shape(self.current_shape)
                if self.check_lose():
                    self.running = False
                    self.root.unbind('<Up>')
                    self.root.unbind('<Down>')
                    self.root.unbind('<Left>')
                    self.root.unbind('<Right>')
                    self.event_log.delete(0, END)
                    self.event_log.insert(0, 'You Lost!')
                self.record_lights(self.current_shape.get_current_shape(*self.current_shape.pivot))

    ##            pprint.pprint([f'Row: {n} is filled' for n in self.check_lights()]) # test
                rows = self.check_lights() # for scoring system
                if rows: # a row is filled
                    self.delete_row(rows)
                del self.current_shape
                self.current_shape = self.next_shape # new shape
                self.next_shape = Game.choose_shape()
                self.display_preview()
                
            self.root.after(GAME_SPEED, self.game_loop)
            
        

if __name__ == '__main__':
    root = Tk()
    game = Game(root) # creating a game object
    root.mainloop()
        








