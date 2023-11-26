import random

from pico2d import load_image, get_time

import attackplayer_topview
import game_framework
import game_world
import play_mode
import state_variable
import topview_mode

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 7.0 # Km / Hour
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
        if state_variable.state_4ball==False:
            if self.situation == 0:
                self.t = self.i / 100
                if self.i<50:
                    self.size = 60 * self.t+10
                else:
                    self.size = 60 * (1-self.t)+10
                self.x = (1 - self.t) * 400 + self.t * state_variable.hit_ballend_x
                self.y = (1 - self.t) * 30 + self.t * (state_variable.hit_ballend_y - 200)
                self.i += 1 * RUN_SPEED_PPS * game_framework.frame_time
                if self.t >= 1:
                    self.i=0
                    self.t = 0
                    self.situation=1
            if self.situation == 1 and state_variable.ball_catch==True:
                self.t = self.i / 100
                self.x = (1 - self.t) *  state_variable.hit_ballend_x + self.t * 490
                self.y = (1 - self.t) * (state_variable.hit_ballend_y - 200) + self.t * 50
                self.i += 1 * RUN_SPEED_PPS * game_framework.frame_time
                if self.t >= 1:
                    if state_variable.atk_safe==False:
                        state_variable.three_out+=1
                        state_variable.atk_life[state_variable.atkplayers_num-1]=-1
                        state_variable.atk_safe=False
                        if state_variable.three_out>=3:
                            state_variable.three_out=0
                            state_variable.strike_num = 0
                            state_variable.ball_num = 0
                    self.situation = -1
                    state_variable.ball_catch=False





