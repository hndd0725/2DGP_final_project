# 이것은 각 상태들을 객체로 구현한 것임.
from random import random

from pico2d import *
from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

import game_framework
import game_world
import play_mode

import state_variable

# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def click(e):
    return e[0]=='INPUT' and e[1].type==SDL_MOUSEBUTTONDOWN
def go_throw(e):
    return e[0] == 'go_throw'
def go_idle(e):
    return e[0] == 'go_idle'
# time_out = lambda e : e[0] == 'TIME_OUT'
#pitcheridle Action Speed
TIME_PER_ACTIONthrow = 1.2
ACTION_PER_TIMEthrow = 1.0 / TIME_PER_ACTIONthrow
FRAMES_PER_ACTIONthrow = 8
FRAMES_PER_ACTIONthrow= FRAMES_PER_ACTIONthrow * ACTION_PER_TIMEthrow#액션프래임속
#batteridle Action Speed
TIME_PER_ACTIONidle = 1
ACTION_PER_TIMEidle = 1.0 / TIME_PER_ACTIONidle
FRAMES_PER_ACTIONidle = 2
FRAMES_PER_ACTIONidle= FRAMES_PER_ACTIONidle * ACTION_PER_TIMEidle#액션프래임속
#batterrun Action Speed
TIME_PER_ACTIONrun = 0.5
ACTION_PER_TIMErun = 1.0 / TIME_PER_ACTIONrun
FRAMES_PER_ACTIONrun = 3
FRAMES_PER_ACTIONrun= FRAMES_PER_ACTIONrun * ACTION_PER_TIMErun#액션프래임속
#
PIXEL_PER_METER = (5 / 0.15) # 10 pixel 30 cm
RUN_SPEED_KMPH = 5.0 # Km / Hour 원래 1
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
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
        batter.frame =(batter.frame + FRAMES_PER_ACTIONrun * ACTION_PER_TIMErun * game_framework.frame_time) % 3
        pass

    @staticmethod
    def draw(batter):
        match int(batter.frame):
            case 0:
                batter.image.clip_draw(225, 70, 17, 25,  batter.x, batter.y, 30,30)
            case 1:

                batter.image.clip_draw(245, 70, 14, 25, batter.x, batter.y, 30, 30)
            case 2:

                batter.image.clip_draw(259, 70, 14, 25, batter.x, batter.y, 30, 30)
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
        batter.frame =(batter.frame + FRAMES_PER_ACTIONidle * ACTION_PER_TIMEidle * game_framework.frame_time) % 2
        pass

    @staticmethod
    def draw(batter):
        match int(batter.frame):
            case 0:
                # if state_variable.atk_loc[0]==0 or state_variable.atk_loc[0]==3:
                   batter.image.clip_draw( 208, 70, 17, 25, batter.x, batter.y, 30, 30)
                # else:
                  #  batter.image.clip_composite_draw(14, 0, 20, 20, 0, 'h', batter.x, batter.y, 20,30)
            case 1:
                # if state_variable.atk_loc[0] == 0 or state_variable.atk_loc[0] == 3:
                     batter.image.clip_draw(225, 70, 17, 25, batter.x, batter.y,30, 30)
                # else:
                   # batter.image.clip_composite_draw(34, 0, 17, 20, 0, 'h', batter.x, batter.y, 20, 30)

class Throw:
    @staticmethod
    def enter(batter, e):
        batter.frame = 0 # pico2d import 필요
        pass

    @staticmethod
    def exit(batter, e):
        pass

    @staticmethod
    def do(batter):
        batter.frame = (batter.frame + FRAMES_PER_ACTIONthrow * ACTION_PER_TIMEthrow * game_framework.frame_time) % 9
    @staticmethod
    def draw(batter):
        match int(batter.frame):
            case 0:
                batter.image.clip_draw(208 + int(batter.frame) * 16, 130, 16, 30, batter.x, batter.y, 30, 30)
            case 1:
                batter.image.clip_draw(208 + int(batter.frame)* 16, 130, 16, 30, batter.x, batter.y, 30, 30)
            case 2:
                batter.image.clip_draw(208 + int(batter.frame) * 16, 130, 16, 30, batter.x, batter.y, 30, 30)
            case 3:
                batter.image.clip_draw(208 + int(batter.frame) * 16, 130, 16, 30, batter.x, batter.y, 30, 30)
            case 4:
                batter.image.clip_draw(208 +int(batter.frame) * 16, 130, 25, 30, batter.x, batter.y, 30, 30)
            case 5:
                batter.image.clip_draw(208 + 4 * 16 + 25, 130, 25, 30, batter.x, batter.y, 30, 30)
            case 6:
                batter.image.clip_draw(208 + 4 * 16 + 25 + 25, 130, 14, 30, batter.x, batter.y, 30, 30)
            case 7:
                batter.image.clip_draw(208 + 4 * 16 + 25 + 25 + 14, 130, 17, 30, batter.x, batter.y, 30, 30)
            case 8:
                batter.image.clip_draw(208 + 4 * 16 + 25 + 25 + 14, 130, 17, 30, batter.x, batter.y, 30, 30)
                batter.state_machine.handle_event(('go_idle', 0))
                state_variable.ball_catch=True
class StateMachine:
    def __init__(self, batter):
        self.batter = batter
        if state_variable.state_4ball == False:
            self.cur_state = Run
        else:
            self.cur_state = Idle
        self.transitions = {
            Idle:{right_down:Run},
            Throw: {go_idle:Idle},
            Run: {go_throw:Throw}
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

class Outfielder:
    def __init__(self):
        self.patrol_locations = [(400, -30),(490, 50), (400, 150), (310, 50), (400, -30),(400, -30)]
        self.x, self.y = 400, 350
        self.indexnum=0
        self.frame = 0
        self.action = 3#오른쪽idle
        self.dir = 0
        self.image = load_image('Baseballplayers.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.state = 'Idle'
        self.situation=0
        self.tx, self.ty = state_variable.hit_ballend_x,(state_variable.hit_ballend_y - 200)
        self.loc_no=0
        self.speed=0
        self.build_behavior_tree()
    def update(self):
        self.state_machine.update()
        if state_variable.state_4ball == False:
            self.bt.run()
    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2
    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
    def move_to(self, r=0.1):
        self.state = 'W'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
    def stop(self):
        if state_variable.atk_loc[self.indexnum]<4:
            if self.state=='W':
                if self.indexnum==0:
                    state_variable.atk_loc[self.indexnum] += 0.5
                else:
                    state_variable.atk_loc[self.indexnum] += 1
                    #print( state_variable.atk_loc[self.indexnum],self.indexnum)
            self.state = 'k'
            self.state_machine.handle_event(('TIME_OUT', 0))
        return BehaviorTree.RUNNING
    def get_patrol_location(self):
        self.tx, self.ty = self.patrol_locations[int(state_variable.atk_loc[self.indexnum]+1)]
        return BehaviorTree.SUCCESS

    def draw_ball(self):
        self.state_machine.handle_event(('go_throw', 0))
        return BehaviorTree.RUNNING
    def build_behavior_tree(self):
        a2 = Action('Move to', self.move_to)
        a1=Action('던지기',self.draw_ball)
        a3=Action('멈춤',self.stop)
        SEQ_run_trow = Sequence('달던,', a2, a1)

        root=SEQ_run_trow
        self.bt = BehaviorTree(root)
    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        #draw_rectangle(*self.get_bb())
        self.state_machine.draw()
    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 10, self.y + 10



