from pico2d import load_image

import game_world


class Ball:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Ball.image == None:
            Ball.image = load_image('baseball.PNG')
        self.x, self.y, self.velocity = x, y, velocity
        self.size=1
        self.t,self.i=0,0

    def draw(self):
        self.image.clip_draw(0, 0, 1500, 1500, self.x, self.y,self.size,self.size)

    def update(self):
            self.t = self.i / 100
            self.size+=10*self.t
            self.x = (1 - self.t) * 420 + self.t * 430
            self.y= (1 - self.t) * 220 + self.t * 80
            self.i += self.velocity
            if(self.t>=1):
                game_world.remove_object(self)
        #game_world.remove_object(self)
        #if self.x<50 or self.x>800-50:
