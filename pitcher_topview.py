# 이것은 각 상태들을 객체로 구현한 것임.
import random

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT

import game_framework
import game_world
from ball import Ball
# state event check
# ( state event type, event value )



def time_out(e):
    return e[0] == 'TIME_OUT'
def hit_out(e):
    return e[0] == 'TIME_OUT'
# time_out = lambda e : e[0] == 'TIME_OUT'
#pitcheridle Action Speed
TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2
FRAMES_PER_ACTION= FRAMES_PER_ACTION * ACTION_PER_TIME#액션프래임속
#pitcheridle Action Speed
TIME_PER_ACTIONthrow = 1.2
ACTION_PER_TIMEthrow = 1.0 / TIME_PER_ACTIONthrow
FRAMES_PER_ACTIONthrow = 8
FRAMES_PER_ACTIONthrow= FRAMES_PER_ACTIONthrow * ACTION_PER_TIMEthrow#액션프래임속


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
        batter.frame = (batter.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    @staticmethod
    def draw(batter):
        match int(batter.frame):
            case 0:
                batter.image.clip_draw(208 + int(batter.frame) * 16, 130, 16, 30, batter.x, batter.y, 20, 30)
            case 1:
                batter.image.clip_draw(208 + int(batter.frame) * 16, 130, 16, 30, batter.x, batter.y, 20, 30)
            case 2:
                batter.image.clip_draw(208 + int(batter.frame) * 16, 130, 16, 30, batter.x, batter.y, 20, 30)
            case 3:
                batter.image.clip_draw(208 + int(batter.frame) * 16, 130, 16, 30, batter.x, batter.y, 20, 30)




class StateMachine:
    def __init__(self, batter):
        self.batter = batter
        self.cur_state = Idle
        self.transitions = {
            Idle: {}

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

class Pitcher:
    def __init__(self):
        self.x, self.y = 400, 50
        self.frame = 0
        self.action = 3#오른쪽idle
        self.dir = 0
        self.face_dir = 1#오른쪽 방향으로 얼굴을 향하고.
        self.image = load_image('Baseballplayers.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.timer=0
    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

