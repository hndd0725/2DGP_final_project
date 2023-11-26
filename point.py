from pico2d import draw_rectangle, load_font

import state_variable

left=0
bottom=0
right=0
top=0

class Point:
    def __init__(self):
        global left,bottom,right,top
        self.x, self.y = 10, 580
        left = self.x
        bottom = self.y
        right = self.x
        top = self.y
        self.font = load_font('ENCR10B.TTF', 25)
    def update(self):
        pass
    def draw(self):
        draw_rectangle(*self.get_bb_strikezone())
        self.font.draw(self.x , self.y , "my_point: " f'{state_variable.my_point}', (0, 255, 255))
        self.font.draw(self.x , self.y-30 , "other_point: " f'{state_variable.other_point}', (255, 0, 255))
        self.font.draw(self.x, self.y - 60, "out: " f'{state_variable.three_out}', (255, 0, 0))
    def get_bb_strikezone(self):
        return left, bottom, right, top

