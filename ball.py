from pico2d import load_image

import game_world

hit_ok=False
class Ball:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1,situation=0):
        if Ball.image == None:
            Ball.image = load_image('baseball.PNG')
        self.x, self.y, self.velocity = x, y, velocity
        self.t,self.i=0,0
        self.timer=0
        self.size = 0
        self.situation=situation
        if self.situation==1 or 2:
            self.size=1
        if self.situation==0:
            self.size = 30
            self.velocity=7
        self.changeball=0
        self.pticher_ballend_x=430
        self.pticher_ballend_y=60

    def draw(self):
        self.image.clip_draw(0, 0, 1500, 1500, self.x, self.y,self.size,self.size)

    def update(self):
        global  hit_ok
        print("hit")
        if self.situation==2:#변화구
                self.t = self.i / 100
                self.size += 5 * self.t
                self.x = (1 - self.t) * 420 + self.t * self.pticher_ballend_x + self.changeball
                self.y = (1 - self.t) * 220 + self.t *  self.pticher_ballend_y
                self.i += self.velocity
                print(self.size)
                if self.i < 50:
                    self.changeball += 5
                if self.i >= 50:
                    self.changeball -= 5
                if hit_ok and 43.75<=self.size and self.size<=48.5 :
                    self.situation = 0
                    self.t = 0
                    self.i = 0
                else:
                    hit_ok=False
                if self.t >= 1:
                    game_world.remove_object(self)
        if self.situation==1:#직선구
                self.t = self.i / 100
                self.size+=5*self.t
                self.x = (1 - self.t) * 420 + self.t * self.pticher_ballend_x + self.changeball
                self.y = (1 - self.t) * 220 + self.t * self.pticher_ballend_y
                self.i += self.velocity
                if hit_ok and 35.0<=self.size and self.size<=39.25:
                    self.situation = 0
                    self.t = 0
                    self.i = 0
                else:
                    hit_ok=False
                if self.t>=1:
                    game_world.remove_object(self)
        if self.situation == 0:  # 타자 칠때
            self.t = self.i / 100
            self.size -= 5 * self.t
            self.x = (1 - self.t) * 430 + self.t * 300
            self.y = (1 - self.t) * 90 + self.t * 550
            self.i += 7
            if (self.t >= 1):
                game_world.remove_object(self)
                hit_ok = False
        #game_world.remove_object(self)
        #if self.x<50 or self.x>800-50:
