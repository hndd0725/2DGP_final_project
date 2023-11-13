# 이것은 각 상태들을 객체로 구현한 것임.
from pico2d import *
from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT


import game_framework
import game_world

import state_variable

# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT



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
TIME_PER_ACTIONrun = 0.5
ACTION_PER_TIMErun = 1.0 / TIME_PER_ACTIONrun
FRAMES_PER_ACTIONrun = 3
FRAMES_PER_ACTIONrun= FRAMES_PER_ACTIONrun * ACTION_PER_TIMErun#액션프래임속
#
PIXEL_PER_METER = (5 / 0.15) # 10 pixel 30 cm
RUN_SPEED_KMPH = 1.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

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
        batter.frame = (batter.frame + FRAMES_PER_ACTIONrun * ACTION_PER_TIMErun * game_framework.frame_time) % 1

    @staticmethod
    def draw(batter):
        # batter.image.clip_draw( 14, 0, 20, 20, batter.x, batter.y, 100, 150)
        # batter.image.clip_draw(34, 0, 17, 20, batter.x, batter.y, 100, 150)
        #batter.image.clip_draw(51, 0, 17, 20, batter.x, batter.y, 50, 60)
        pass


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
        batter.frame = (batter.frame + FRAMES_PER_ACTIONrun * ACTION_PER_TIMErun * game_framework.frame_time) % 3
        pass

    @staticmethod
    def draw(batter):
        match int(batter.frame):
            case 0:
                batter.image.clip_draw( 14, 0, 20, 20, batter.x, batter.y, 20, 30)
            case 1:
                batter.image.clip_draw(34, 0, 17, 20, batter.x, batter.y, 20, 30)
            case 2:
                batter.image.clip_draw(51, 0, 17, 20, batter.x, batter.y, 20, 30)

class StateMachine:
    def __init__(self, batter):
        self.batter = batter
        self.cur_state = Run
        self.transitions = {
            Idle: {right_down: Run},
            Run: {}

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

class AtkPlayer:
    def __init__(self):
        self.x, self.y = 400, -30#오른쪽 베이스490,60
        self.frame = 0
        self.action = 3#오른쪽idle
        self.dir = 0
        self.face_dir = 1#오른쪽 방향으로 얼굴을 향하고.
        self.image = load_image('Baseballplayers.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.timer=0
        self.i=0
        self.t=0
        self.situation=0
    def update(self):
        self.state_machine.update()
        if self.situation == 0:
            global ballhit_start_x, ballhit_start_y
            self.t = self.i / 100
            if self.i<50:
                self.size = 60 * self.t+10
            else:
                self.size = 60 * (1-self.t)+10
            self.x = (1 - self.t) * 400 + self.t * 490
            self.y = (1 - self.t) * -30 + self.t * 60
            self.i += 1 * RUN_SPEED_PPS * game_framework.frame_time
            if self.t >= 1:
                self.situation=-1
    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()




