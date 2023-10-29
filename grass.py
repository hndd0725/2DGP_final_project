from pico2d import load_image


class Grass:
    def __init__(self):
        self.image = load_image('baseball stadium1.png')

    def draw(self):
        self.image.clip_draw(0, 0, 500, 500,400,300,800,600)

    def update(self):
        pass
