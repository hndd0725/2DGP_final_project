from pico2d import draw_rectangle


class Strikezone:
    def __init__(self):
        self.x, self.y = 320, 120
        self.left= self.x - 20 + 100
        self.bottom=self.y - 35
        self.right= self.x + 20 + 100
        self.top=self.y + 20
    def update(self):
        pass
    def draw(self):
        draw_rectangle(*self.get_bb_strikezone())
    def get_bb_strikezone(self):
        return self.left, self.bottom, self.right, self.top

