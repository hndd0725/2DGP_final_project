# 이것은 각 상태들을 객체로 구현한 것임.
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
def time_out(e):
    return e[0] == 'TIME_OUT'

# time_out = lambda e : e[0] == 'TIME_OUT'

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
RUN_SPEED_KMPH = 10.0 # Km / Hour 원래 1
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Idle:

    @staticmethod
    def enter(batter, e):
        global logo_start_time
        batter.frame = 0
        logo_start_time = get_time()
        state_variable.atk_loc[0] += 1
        pass

    @staticmethod
    def exit(batter, e):
        pass

    @staticmethod
    def do(batter):
        batter.frame = (batter.frame + FRAMES_PER_ACTIONidle * ACTION_PER_TIMEidle * game_framework.frame_time) % 2
        if get_time() - logo_start_time >= 2.0:
            game_framework.change_mode(play_mode)
    @staticmethod
    def draw(batter):
        match int(batter.frame):
            case 0:
                batter.image.clip_composite_draw(0, 20, 15, 20,0,'h', batter.x, batter.y, 20, 30)
            case 1:
                batter.image.clip_composite_draw(35, 20, 15, 25, 0, 'h', batter.x, batter.y, 20, 30)
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
                if state_variable.atk_loc[0]==0 or state_variable.atk_loc[0]==3:
                    batter.image.clip_draw( 14, 0, 20, 20, batter.x, batter.y, 20, 30)
                else:
                    batter.image.clip_composite_draw(14, 0, 20, 20, 0, 'h', batter.x, batter.y, 20,30)
            case 1:
                if state_variable.atk_loc[0] == 0 or state_variable.atk_loc[0] == 3:
                    batter.image.clip_draw(34, 0, 17, 20, batter.x, batter.y, 20, 30)
                else:
                    batter.image.clip_composite_draw(34, 0, 17, 20, 0, 'h', batter.x, batter.y, 20, 30)
            case 2:
                if state_variable.atk_loc[0] == 0 or state_variable.atk_loc[0] == 3:
                    batter.image.clip_draw(51, 0, 17, 20, batter.x, batter.y, 20, 30)
                else:
                    batter.image.clip_composite_draw(51, 0, 17, 20, 0, 'h', batter.x, batter.y, 20, 30)

class StateMachine:
    def __init__(self, batter):
        self.batter = batter
        self.cur_state = Run
        self.transitions = {
            Idle: {right_down: Run},
            Run: {time_out:Idle}

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
    def __init__(self,num):
        self.patrol_locations = [(400, -30),(490, 50), (400, 150), (310, 50), (400, -30),(400, -30)]
        self.x, self.y = self.patrol_locations[state_variable.atk_loc[num]]#오른쪽 베이스490,50
        self.indnum=num
        self.frame = 0
        self.action = 3#오른쪽idle
        self.dir = 0
        self.face_dir = 1#오른쪽 방향으로 얼굴을 향하고.
        self.image = load_image('Baseballplayers.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.state = 'Idle'
        self.i=0
        self.t=0
        self.situation=0
        self.tx, self.ty = 1000, 1000
        self.loc_no=0
        self.speed=0
        self.build_behavior_tree()


    def update(self):
        self.state_machine.update()
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
        self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
    def stop(self):
        self.state = 'Idel'
        self.state_machine.handle_event(('TIME_OUT', 0))
        return BehaviorTree.RUNNING
    def get_patrol_location(self):
        self.tx, self.ty = self.patrol_locations[state_variable.atk_loc[self.indnum]+1]
        return BehaviorTree.SUCCESS
    def is_home_finish(self):
        if self.loc_no<=4:
            return BehaviorTree.SUCCESS
        else:
            self.state_machine.handle_event(('TIME_OUT', 0))
            return  BehaviorTree.FAIL
    def build_behavior_tree(self):
        a2 = Action('Move to', self.move_to)
        a1=Action('달리기위치 가져오기',self.get_patrol_location)
        a3=Action('멈춤',self.stop)
        c1=Condition('홈까지 도착?',self.is_home_finish)
        SEQ_patrol = Sequence('달리기', a1, a2)
        SEQ_homrun = Sequence('모든베이스달리기', c1,a1, a2)
        root = SEQ_go_stop = Sequence('달리기하며 도착시 멈춤', SEQ_patrol, a3)
        #root = SEQ_homrun
        self.bt = BehaviorTree(root)
    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()




