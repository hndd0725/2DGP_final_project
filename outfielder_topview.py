from pico2d import *

import random
import math
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import topview_mode


# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk', 'Idle']


class Outfielder:
    images = None

    def load_images(self):
        if Outfielder.images == None:
            # Outfielder.images = {}
            # for name in animation_names:
            #     Outfielder.images[name] = [load_image("./zombie/" + name + " (%d)" % i + ".png") for i in range(1, 11)]
            # Outfielder.font = load_font('ENCR10B.TTF', 40)
            pass

    def __init__(self, x=None, y=None):
        self.x = x if x else random.randint(100, 1180)
        self.y = y if y else random.randint(100, 924)
        self.load_images()
        self.dir = 0.0      # radian 값으로 방향을 표시
        self.speed = 0.0
        self.frame = random.randint(0, 9)
        self.state = 'Idle'
        self.ball_count = 0
        self.image = load_image('Baseballplayers.png')
        self.tx,self.ty=1000,1000
        self.build_behavior_tree()

        self.patrol_locations = [(43, 274), (1118, 274), (1050, 494), (575, 804), (235, 991), (575, 804), (1050, 494),
                                 (1118, 274)]
        self.loc_no = 0


    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50


    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        # fill here
        self.bt.run()

    def draw(self):
        if math.cos(self.dir) < 0:
            Outfielder.images[self.state][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
        else:
            Outfielder.images[self.state][int(self.frame)].draw(self.x, self.y, 100, 100)
        self.font.draw(self.x - 10, self.y + 60, f'{self.ball_count}', (0, 0, 255))
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'zombie:ball':
            self.ball_count += 1

    def set_target_location(self, x=None, y=None):
        if not x or not y:
            raise ValueError('Location should be given')
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    def move_to(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING


    def set_random_location(self):
        self.tx, self.ty = random.randint(100, 1280 - 100), random.randint(100, 1024 - 100)
        return BehaviorTree.SUCCESS

    def is_boy_nearby(self, r):
        if self.distance_less_than(topview_mode.AtkPlayer.x, topview_mode.AtkPlayer.y, self.x, self.y, r) :
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_boy(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(topview_mode.AtkPlayer.x, topview_mode.AtkPlayer.y)
        if self.distance_less_than(topview_mode.AtkPlayer.x, topview_mode.AtkPlayer.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def escape_to_boy(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(2*self.topview_mode.AtkPlayer.x,2*self.y-topview_mode.AtkPlayer.y)
        if self.distance_less_than(topview_mode.AtkPlayer.x, topview_mode.AtkPlayer.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING


    def get_patrol_location(self):
        self.tx, self.ty = self.patrol_locations[self.loc_no]
        self.loc_no = (self.loc_no + 1) % len(self.patrol_locations)
        return BehaviorTree.SUCCESS


    def build_behavior_tree(self):
        a1 = Action('Set target location', self.set_target_location, 500, 50)
        a2 = Action('Move to', self.move_to)
        SEQ_move_to_target_location = Sequence('Move to target location', a1, a2)
        a3 = Action('Set random location', self.set_random_location)
        root = SEQ_wander = Sequence('Wander', a3, a2)
        #c1 = Condition('소년이 근처에 있는가?', self.is_boy_nearby, 7)
        # c2 = Condition('소년이 근처에 있는가?', self.is_boy_nearby2, 7)
        a4 = Action('소년한테 접근', self.move_to_boy)
        a5 = Action('소년한테 도망', self.escape_to_boy)
        # SEQ_chase_boy = Sequence('소년을 추적', c1, a4)
        # SEQ_chase_boy2 = Sequence('소년 도망', c2, a5)
        # root = SEL_chase_or_flee = Selector('추적 또는 배회', SEQ_chase_boy,SEQ_chase_boy2, SEQ_wander)
        # a5 = Action('순찰 위치 가져오기', self.get_patrol_location)
        #root = SEQ_patrol = Sequence('순찰', c1, a2)
        self.bt = BehaviorTree(root)