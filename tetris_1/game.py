from tkinter import *
from tkinter import simpledialog
import random
import datetime
import csv
from constants import GAME_SPEED, BG_COLOUR, BD_WIDTH
from tile import Tile
from line_shape import LineShape
from square_shape import SquareShape
from t_shape import TShape
from l_shape_left import LShapeLeft
from l_shape_right import LShapeRight
from z_shape_left import ZShapeLeft
from z_shape_right import ZShapeRight


class Game:

    shapes = ('line', 'square', 't', 'l_left', 'l_right', 'z_left', 'z_right')
    shape_record = [] # to hold names of all instantiated objects
    
    def __init__(self, root):
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
        if not self.event_handler:
            self.event_handler = True
            if self.current_shape.check_rotation_collision(self.all_buttons, *self.current_shape.pivot) == True:
                self.current_shape.erase_shape(self.all_buttons, self.current_shape.pivot[0], self.current_shape.pivot[1])
                self.current_shape.erase_shape(self.all_buttons, self.current_shape.pivot[0]-1, self.current_shape.pivot[1])
                self.current_shape.rotate(self.all_buttons)
            elif self.current_shape.check_rotation_collision(self.all_buttons, *self.current_shape.pivot) == 'left':
                self.current_shape.set_pivot(self.current_shape.pivot[0], self.current_shape.pivot[1]-1)
                self.current_shape.erase_shape(self.all_buttons, self.current_shape.pivot[0], self.current_shape.pivot[1])
                self.current_shape.erase_shape(self.all_buttons, self.current_shape.pivot[0], self.current_shape.pivot[1]+1)
                self.current_shape.rotate(self.all_buttons)
            elif self.current_shape.check_rotation_collision(self.all_buttons, *self.current_shape.pivot) == 'right':
                self.current_shape.set_pivot(self.current_shape.pivot[0], self.current_shape.pivot[1]+1)
                self.current_shape.erase_shape(self.all_buttons, self.current_shape.pivot[0], self.current_shape.pivot[1])
                self.current_shape.erase_shape(self.all_buttons, self.current_shape.pivot[0], self.current_shape.pivot[1]-1)
                self.current_shape.rotate(self.all_buttons)
            self.event_handler = False

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

        mode_frame = LabelFrame(self.root, text='Game mode', padx=4, pady=4)
        mode_frame.configure(bg='#3d3d3d')
        mode_frame.grid(row=5, column=25)
        self.mode = StringVar()
        self.mode.set('Marathon')
        self.marathon = Radiobutton(mode_frame, text='Marathon', bg='light blue', variable=self.mode, value='Marathon').pack()
        self.touchdown = Radiobutton(mode_frame, text='Touchdown', bg='light blue', variable=self.mode, value='Touchdown').pack()
        
        settings = LabelFrame(self.root, padx=0, pady=0)
        settings.grid(row=0, column=0)
        settings_button = Button(settings, text='⚙', padx=5, pady=5, borderwidth=0.7, command=self.customize)
        settings_button.grid(row=0, column=0)
        self.game_type = Label(settings, text=f'Mode: {self.mode.get()}', font=('Arial', 16, 'italic'))
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

        self.root.bind('<Return>', lambda event: self.start_game())
        # next shape preview
        self.display_preview()


    def customize(self):
        self.top = Toplevel()
        customize = LabelFrame(self.top, text='settings')
        customize.grid(row=0, column=0, padx=5, pady=5)
        # speed
        speed_frame = LabelFrame(customize) # nested frame widgets for organization
        speed_frame.grid(row=0, column=0, padx=2) 
        Label(speed_frame, text='Speed', font=('Arial', 12, 'bold')).grid(row=0, column=0)
        
        chosen_speed = StringVar()
        chosen_speed.set('0.8')
        all_speeds = (
            ('Ultra Fast', '0.4'),
            ('Fast', '0.5'),
            ('Normal', '0.8'),
            ('Slow', '1')
            )
        row = 1
        for speed, identifier in all_speeds:
            r = Radiobutton(speed_frame, text=speed, variable=chosen_speed, value=identifier)
            r.grid(row=row, column=0)
            row += 1
        # spacer
        Label(customize, text='   ').grid(row=0, column=1)
        # background colour
        bg_frame = LabelFrame(customize)
        bg_frame.grid(row=0, column=1, padx=2)
        Label(bg_frame, text='Background', font=('Arial', 12, 'bold')).grid(row=0, column=3)
        
        chosen_colour = StringVar()
        chosen_colour.set('black')
        all_colours = (
            ('black', 'black'),
            ('grey', 'grey'),
            ('papayawhip', 'papayawhip'),
            ('lavenderblush', 'lavenderblush'),
            ('mintcream', 'mintcream'),
            ('white', 'white')
            )
        row = 1
        for bg, identifier in all_colours:
            f = Frame(bg_frame, bd=3, relief=SOLID)
            f.grid(row=row, column=2, pady=2)
            Label(f, padx=5, bg=bg).grid(row=row, column=2)
            r = Radiobutton(bg_frame, text=bg, variable=chosen_colour, value=identifier)
            r.grid(row=row, column=3)
            row += 1
        # need to add borderwidth user option as well
        # remember to change window geometry
            
        submission = LabelFrame(self.top)
        submission.grid(row=1, column=0, pady=5)
        save = Button(
            submission, text='Save changes', borderwidth=2, bg='papayawhip', command=lambda: self.save_prefrences(
                self.top, float(chosen_speed.get())*1000, chosen_colour.get(), bd_width=1))
        Label(submission, text='   ').grid(row=0, column=1) # spacer
        cancel = Button(
            submission, text='Cancel', borderwidth=2, bg='papayawhip', command=lambda: self.top.destroy())
        save.grid(row=0, column=0)
        cancel.grid(row=0, column=2)

    @staticmethod
    def save_prefrences(window, speed:float, bg_colour:str, bd_width:int):
        with open('constants.py', 'w') as f:
            f.write('GAME_SPEED = {}\n'.format(str(int(speed))))
            f.write('BG_COLOUR = "{}"\n'.format(bg_colour))
            f.write('BD_WIDTH = {}\n'.format(bd_width))
        window.destroy()

        
    def start_game(self):
        # key - settings
        print('Game started')
        self.score.configure(text='0')
        # determining setup for different modes
        if self.mode.get() == 'Touchdown':
            self.game_type.configure(text=f'Mode: {self.mode.get()}')
            all_colours = [LineShape().colour,
                           SquareShape().colour,
                           TShape().colour,
                           LShapeLeft().colour,
                           LShapeRight().colour,
                           ZShapeLeft().colour,
                           ZShapeRight().colour]
            for i in range(15, 21):
                for j in range(10):
                    choice = random.randint(0, 1)
                    if choice == 1:
                        self.all_buttons[i][j].configure(bg=random.choice(all_colours))
                        self.all_buttons[i][j].on = True
                    
        self.root.bind('<Up>',  lambda event: self.up_key_press())
        self.root.bind('<Left>',  lambda event: self.left_key_press())
        self.root.bind('<Right>',  lambda event: self.right_key_press())
        self.root.bind('<Down>', lambda event: self.down_key_press())
        self.root.bind('p', lambda event: self.pause())
        self.event_log.insert(0, 'Game started! (p to pause)')
        self.root.unbind('<Return>')
        self.running = True
        self.game_loop()

    def pause(self):
        self.event_log.delete(0, END)
        if self.running:
            self.running = False
            self.event_log.insert(0, 'Paused')
        elif not self.running:
            self.running = True
            self.game_loop()

    def clear_board(self):
        for row in self.all_buttons:
            for button in row:
                button.configure(bg=BG_COLOUR)
                button.on = False
        self.root.bind('<Return>', lambda event: self.start_game())
        root.unbind('p')

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
#        test
##        for row in self.all_buttons:
##            print(''.join(['1' if b.on else '0' for b in row]))
##        print()
        for button in self.all_buttons[1]:
            if button.on:
                return True
        return False

    def check_win(self): # for touchdown mode
        for i in range(10, 21):
            for j in range(10):
                if not self.all_buttons[i][j].on and self.all_buttons[i-1][j].on:
                    return False
        return True

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

            # hit the bottom
            else:
                Game.record_shape(self.current_shape)
                self.record_lights(self.current_shape.get_current_shape(*self.current_shape.pivot))

    ##            pprint.pprint([f'Row: {n} is filled' for n in self.check_lights()]) # test
                rows = self.check_lights() # for scoring system
                if rows: # a row is filled
                    self.delete_row(rows)
                del self.current_shape
                self.current_shape = self.next_shape # new shape
                self.next_shape = Game.choose_shape()
                self.display_preview()
                
                if self.check_lose():
                    self.running = False
                    self.root.unbind('<Up>')
                    self.root.unbind('<Down>')
                    self.root.unbind('<Left>')
                    self.root.unbind('<Right>')
                    self.root.unbind('p')
                    self.event_log.delete(0, END)
                    self.event_log.insert(0, 'You Lost!')
                    Game.shape_record.clear()
                    
                    # saving score and ask for initials
                    initials = ' '
                    try:
                        with open('high_scores.csv') as f:
                            # checking for high score
                            current_score = int(self.score.cget('text'))
                            reader = csv.reader(f)
                            statement = [int(row[2])<=current_score for row in reader if row]
                            if all(statement):
                                self.event_log.delete(0, END)
                                self.event_log.insert(0, 'New high score!')
                                initials = simpledialog.askstring('input', 'New high score!\nName / Nickname: ')
                                if not initials:
                                    initials = 'Anonymous'
                    except:
                        pass
                            
                    with open('high_scores.csv', mode='a') as f:
                        date = datetime.datetime.today()
                        today = str(date.day)+'/'+str(date.month)+'/'+str(date.year)
                        data = [today, initials, int(self.score.cget('text'))]
                        writer = csv.writer(f)
                        writer.writerow(data)
                elif self.check_win() and self.mode.get() == 'Touchdown':
                    self.running = False
                    self.root.unbind('<Up>')
                    self.root.unbind('<Down>')
                    self.root.unbind('<Left>')
                    self.root.unbind('<Right>')
                    self.root.unbind('p')
                    self.event_log.delete(0, END)
                    self.event_log.insert(0, f'You win! ({len(Game.shape_record)} shapes)')
                    self.shape_record.clear()
                
            self.root.after(GAME_SPEED, self.game_loop)
            
        else:
            self.root.bind('<Return>', lambda event: self.clear_board())
            


if __name__ == '__main__':
    root = Tk()
    game = Game(root) # creating a game object
    root.mainloop()
