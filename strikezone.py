from pico2d import draw_rectangle

left=0
bottom=0
right=0
top=0
class Strikezone:
    def __init__(self):
        global left,bottom,right,top
        self.x, self.y = 320, 120
        left = self.x - 20 + 100
        bottom = self.y - 35
        right = self.x + 20 + 100
        top = self.y + 20

    def update(self):
        pass
    def draw(self):
        draw_rectangle(*self.get_bb_strikezone())
    def get_bb_strikezone(self):
        return left, bottom, right, top

