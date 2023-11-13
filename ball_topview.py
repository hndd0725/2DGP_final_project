import random

from pico2d import load_image

import game_framework
import game_world
import state_variable
import strikezone
import topview_mode



PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 5.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
class Ball:
    image = None

    def __init__(self, x = 400, y = 30):
        if Ball.image == None:
            Ball.image = load_image('baseball.PNG')
        self.x, self.y, self.velocity = x, y,1
        self.t,self.i=0,0
        self.timer=0
        self.situation=0
        self.size = 10.0

    def draw(self):
        self.image.clip_draw(0, 0, 1500, 1500, self.x, self.y,self.size,self.size)

    def update(self):
        if self.situation == 0:
            global ballhit_start_x, ballhit_start_y
            self.t = self.i / 100
            if self.i<50:
                self.size = 60 * self.t+10
            else:
                self.size = 60 * (1-self.t)+10
            self.x = (1 - self.t) * 400 + self.t * state_variable.hit_ballend_x
            self.y = (1 - self.t) * 30 + self.t * (state_variable.hit_ballend_y - 200)
            self.i += 1 * RUN_SPEED_PPS * game_framework.frame_time
            if self.t >= 1:
                self.situation=-1




