import random

from pico2d import load_image

import game_framework
import game_world
import state_variable
import strikezone
import topview_mode



PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
class Ball:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1,situation=0):
        if Ball.image == None:
            Ball.image = load_image('baseball.PNG')
        self.x, self.y, self.velocity = x, y, velocity
        self.t,self.i=0,0
        self.timer=0
        self.size = 0.0
        self.situation=situation
        if self.situation==1 or 2:
            self.size=1.0
        if self.situation==0:
            self.size = 30.0
            self.velocity=7
        self.changeball=0
        self.throw_ballend_x=random.randint(strikezone.left, strikezone.right)#430
        self.throw_ballend_y=random.randint(strikezone.bottom, strikezone.top)#100
        state_variable.hit_ballend_x=random.randint(80, 550)
        state_variable.hit_ballend_y=random.randint(400, 900)
    def draw(self):
        self.image.clip_draw(0, 0, 1500, 1500, self.x, self.y,self.size,self.size)

    def update(self):

        global ballhit_start_x,ballhit_start_y
        if self.situation==2:#변화구
                self.t = self.i / 100
                self.size = 30 * self.t
                self.x = (1 - self.t) * 420 + self.t * self.throw_ballend_x + self.changeball
                self.y = (1 - self.t) * 220 + self.t *  self.throw_ballend_y
                self.i += 1 * RUN_SPEED_PPS * game_framework.frame_time #self.velocity
                if self.i < 50:
                    self.changeball += 1
                if self.i >= 50:
                    self.changeball -= 1
                if state_variable.hit_ok and 24.0 <= self.size:

                    ballhit_start_x=self.x
                    ballhit_start_y = self.y
                    self.situation = 0
                    self.t = 0
                    self.i = 0
                    state_variable.atkplayers_num+=1

                else:
                    state_variable.hit_ok=False
                if self.t >= 1:
                    game_world.remove_object(self)
        if self.situation==1:#직선구
                self.t = self.i / 100
                self.size=30*self.t
                self.x = (1 - self.t) * 420 + self.t * self.throw_ballend_x
                self.y = (1 - self.t) * 220 + self.t * self.throw_ballend_y
                self.i += 1 * RUN_SPEED_PPS * game_framework.frame_time
                if state_variable.hit_ok and 15.0<=self.size:
                    ballhit_start_x=self.x
                    ballhit_start_y = self.y
                    self.situation = 0
                    self.t = 0
                    self.i = 0
                    state_variable.atkplayers_num += 1
                else:
                    state_variable.hit_ok=False
                if self.t>=1:
                    game_world.remove_object(self)
        if self.situation == 0:  # 타자 칠때
            self.t = self.i / 100
            self.size = 30 * (1-self.t)
            self.x = (1 - self.t) * ballhit_start_x + self.t *state_variable.hit_ballend_x
            self.y = (1 - self.t) * ballhit_start_y + self.t *state_variable.hit_ballend_y
            self.i += 1 * RUN_SPEED_PPS * game_framework.frame_time
            if self.t >= 1:
                game_world.remove_object(self)
                game_framework.change_mode(topview_mode)
                state_variable.hit_ok = False

