import random

from pico2d import load_image, load_wav

import ballzone
import game_framework
import game_world
import lose_mode
import play_mode
import state_variable
import strikezone
import topview_mode
import win_mode

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 13.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
class Ball:
    image = None
    hit_sound=None
    def __init__(self, x = 400, y = 300, velocity = 1,situation=0):
        if Ball.image == None:
            Ball.image = load_image('baseball.PNG')
            Ball.hit_sound=load_wav('hit_sound.wav')
            Ball.hit_sound.set_volume(32)
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
        self.throw_ballend_x=random.randint(ballzone.left, ballzone.right)#430
        self.throw_ballend_y=random.randint(ballzone.bottom, ballzone.top)#100
        state_variable.hit_ballend_x=random.randint(80, 550)
        if self.throw_ballend_x<=strikezone.left and self.throw_ballend_y>=strikezone.bottom and self.throw_ballend_y<=strikezone.top:
            state_variable.hit_ballend_y=random.randint(500, 700)
        else:
            state_variable.hit_ballend_y = random.randint(400, 500)
        self.one_swing=0
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
                if state_variable.swing and 26.0 <= self.size:
                    ballhit_start_x=self.x
                    ballhit_start_y = self.y
                    self.situation = 0
                    self.t = 0
                    self.i = 0
                    state_variable.strike_num = 0
                    state_variable.ball_num = 0
                    state_variable.atkplayers_num+=1
                    Ball.hit_sound.play()
                elif state_variable.swing and 26.0 > self.size:
                    if self.one_swing==0:
                        state_variable.strike_num+=1
                        self.one_swing=-1
                    state_variable.is_swing_more_one += 1
                if self.t >= 1:
                    if state_variable.is_swing_more_one==0:
                        if strikezone.left <= self.throw_ballend_x <= strikezone.right and strikezone.bottom <= self.throw_ballend_y <= strikezone.top:
                            state_variable.strike_num += 1
                        else:
                            state_variable.ball_num += 1
                    state_variable.swing = False
                    state_variable.is_swing_more_one = 0
                    game_world.remove_object(self)
                if state_variable.strike_num==3:
                    state_variable.strike_num=0
                    state_variable.ball_num=0
                    state_variable.three_out += 1
                    if state_variable.three_out >= 3:
                        state_variable.three_out = 0
                        state_variable.strike_num = 0
                        state_variable.ball_num = 0
                        state_variable.atk_loc = [0 for _ in range(0, 100)]
                        state_variable.atk_life = [0 for _ in range(0, 100)]
                        state_variable.game_num += 1
                        state_variable.atkplayers_num = 0
                        state_variable.other_point += random.randint(0, 5)
                        if state_variable.game_num==3:
                            if state_variable.my_point>=state_variable.other_point:
                                game_framework.change_mode(win_mode)
                            else:
                                game_framework.change_mode(lose_mode)
                        else:
                            game_framework.change_mode(play_mode)

                elif state_variable.ball_num==4:
                    state_variable.strike_num = 0
                    state_variable.ball_num = 0
                    state_variable.atkplayers_num += 1
                    state_variable.state_4ball = True
                    # game_world.remove_object(self)
                    game_framework.change_mode(topview_mode)
        if self.situation==1:#직선구
                self.t = self.i / 100
                self.size=30*self.t
                self.x = (1 - self.t) * 420 + self.t * self.throw_ballend_x
                self.y = (1 - self.t) * 220 + self.t * self.throw_ballend_y
                self.i += 1 * RUN_SPEED_PPS * game_framework.frame_time
                print(self.size)
                if state_variable.swing and 26.0<=self.size:
                    ballhit_start_x=self.x
                    ballhit_start_y = self.y
                    self.situation = 0
                    self.t = 0
                    self.i = 0
                    state_variable.strike_num=0
                    state_variable.ball_num = 0
                    state_variable.atkplayers_num += 1
                    state_variable.is_swing_more_one+=1
                    Ball.hit_sound.play()
                elif state_variable.swing and 26.0 > self.size:
                    if self.one_swing == 0:
                        state_variable.strike_num += 1
                        self.one_swing = -1
                    state_variable.is_swing_more_one += 1
                if self.t>=1:
                    if state_variable.is_swing_more_one==0:
                        if strikezone.left<=self.throw_ballend_x <=strikezone.right and strikezone.bottom<=self.throw_ballend_y<=strikezone.top:
                            state_variable.strike_num += 1
                        else:
                            state_variable.ball_num += 1
                    state_variable.swing = False
                    state_variable.is_swing_more_one = 0
                    game_world.remove_object(self)
                if state_variable.strike_num==3:
                    state_variable.strike_num=0
                    state_variable.ball_num=0
                    state_variable.three_out+=1
                    if state_variable.three_out>=3:
                        state_variable.three_out = 0
                        state_variable.strike_num = 0
                        state_variable.ball_num = 0
                        state_variable.atk_loc = [0 for _ in range(0, 100)]
                        state_variable.atk_life = [0 for _ in range(0, 100)]
                        state_variable.atkplayers_num = 0
                        state_variable.game_num +=1
                        state_variable.other_point += random.randint(0, 5)
                        if state_variable.game_num == 3:
                            if state_variable.my_point >= state_variable.other_point:
                                game_framework.change_mode(win_mode)
                            else:
                                game_framework.change_mode(lose_mode)
                        else:
                            game_framework.change_mode(play_mode)
                elif state_variable.ball_num==4:
                    state_variable.strike_num = 0
                    state_variable.ball_num = 0
                    state_variable.atkplayers_num += 1
                    state_variable.state_4ball=True
                    #game_world.remove_object(self)
                    game_framework.change_mode(topview_mode)

        if self.situation == 0:  # 타자 칠때
            self.t = self.i / 100
            self.size = 30 * (1-self.t)
            self.x = (1 - self.t) * ballhit_start_x + self.t *state_variable.hit_ballend_x
            self.y = (1 - self.t) * ballhit_start_y + self.t *state_variable.hit_ballend_y
            self.i += 1 * RUN_SPEED_PPS * game_framework.frame_time
            if self.t >= 1:
                game_world.remove_object(self)
                state_variable.is_swing_more_one = 0
                state_variable.swing = False
                game_framework.change_mode(topview_mode)


