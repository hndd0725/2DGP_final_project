# 이것은 각 상태들을 객체로 구현한 것임.
from pico2d import *
from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT

import random
import math
import game_framework
import game_world
from ball import Ball
import state_variable

# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def click(e):
    return e[0]=='INPUT' and e[1].type==SDL_MOUSEBUTTONDOWN
def hit_out(e):
    return e[0] == 'TIME_OUT'
# time_out = lambda e : e[0] == 'TIME_OUT'

#batterhit Action Speed
TIME_PER_ACTIONhit = 0.6
ACTION_PER_TIMEhit = 1.0 / TIME_PER_ACTIONhit
FRAMES_PER_ACTIONhit = 6
FRAMES_PER_ACTIONhit= FRAMES_PER_ACTIONhit * ACTION_PER_TIMEhit#액션프래임속
#batteridle Action Speed
TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2
FRAMES_PER_ACTION= FRAMES_PER_ACTION * ACTION_PER_TIME#액션프래임속

class Idle:

    @staticmethod
    def enter(batter, e):
        batter.frame = 0
        pass

    @staticmethod
    def exit(batter, e):
        pass

    @staticmethod
    def do(batter):
        batter.frame = (batter.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2

    @staticmethod
    def draw(batter):
        batter.image.clip_draw(int(batter.frame) * 16, 90, 16, 40, batter.x, batter.y, 100, 250)


class Run:
    @staticmethod
    def enter(batter, e):
        batter.frame = 0
        pass

    @staticmethod
    def exit(batter, e):

        pass

    @staticmethod
    def do(batter):
        batter.frame = (batter.frame + FRAMES_PER_ACTIONhit * ACTION_PER_TIMEhit * game_framework.frame_time) % 6

        pass

    @staticmethod
    def draw(batter):
        pass


class Hit:
    @staticmethod
    def enter(batter, e):
        batter.frame = 0 # pico2d import 필요

        pass

    @staticmethod
    def exit(batter, e):
        pass

    @staticmethod
    def do(batter):
        batter.frame = (batter.frame + FRAMES_PER_ACTIONhit * ACTION_PER_TIMEhit * game_framework.frame_time) % 6

    @staticmethod
    def draw(batter):
        match int(batter.frame):
            case 0:
                batter.image.clip_draw(int(batter.frame) * 16, 90, 16, 40, batter.x, batter.y, 100, 250)
            case 1:
                batter.image.clip_draw(int(batter.frame) * 16, 90, 16, 40, batter.x, batter.y, 100, 250)
            case 2:
                batter.image.clip_draw(32, 90, 30, 40, batter.x + 50, batter.y, 200, 250)
            case 3:
                batter.image.clip_draw(62, 90, 30, 40, batter.x + 50, batter.y, 200, 250)
                state_variable.swing = True
            case 4:
                batter.image.clip_draw(92, 90, 25, 40, batter.x + 50, batter.y, 200, 250)
            case 5:
                batter.image.clip_draw(117, 90, 25, 38, batter.x, batter.y, 200, 250)
                batter.state_machine.handle_event(('TIME_OUT', 0))




class StateMachine:
    def __init__(self, batter):
        self.batter = batter
        self.cur_state = Idle
        self.transitions = {
            Idle: {click:Hit, right_down: Run, left_down: Run, left_up: Run, right_up: Run},
            Run: {space_down:Run,right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
            Hit: {hit_out:Idle}
        }

    def start(self):
        self.cur_state.enter(self.batter, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.batter)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.batter, e)
                self.cur_state = next_state
                self.cur_state.enter(self.batter, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.batter)

class Batter:
    def __init__(self):
        self.x, self.y = 320, 120
        self.frame = 0
        self.action = 3#오른쪽idle
        self.dir = 0
        self.face_dir = 1#오른쪽 방향으로 얼굴을 향하고.
        self.image = load_image('Baseballplayers.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.timer=0
        self.font = load_font('ENCR10B.TTF', 25)
    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x - 200, self.y + 60,"Strike " f'{ state_variable.strike_num}', (255, 0, 0))
        self.font.draw(self.x - 200, self.y + 40, "Ball " f'{state_variable.ball_num}', (0, 0, 255))



    def fire_ball(self,sit):
        ball=Ball(self.x,self.y,5,sit)
        game_world.add_object(ball,1)


