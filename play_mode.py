from pico2d import *

import game_world
import play_mode
import state_variable
from ballzone import Ballzone

from batter import Batter
from grass import Grass
import game_framework
from pitcher import Pitcher
from point import Point
from strikezone import Strikezone


# Game object class here

bgm2=None
def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
        #     game_framework.change_mode(title_mode)
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
        #     game_framework.push_mode(item_mode)#finish호출안됌
        else:
            batter.handle_event(event)
            pitcher.handle_event(event)


def init():
    global grass
    global batter
    global pitcher
    global strikezone
    global ballzone
    global point
    global bgm

    grass = Grass()
    game_world.add_object(grass, 0)
    batter = Batter()
    game_world.add_object(batter, 2)
    pitcher = Pitcher()
    game_world.add_object(pitcher, 2)
    strikezone=Strikezone()
    game_world.add_object(strikezone, 2)
    ballzone = Ballzone()
    game_world.add_object(ballzone, 2)
    point = Point()
    game_world.add_object(point, 2)
    if play_mode.bgm2==None:
        bgm = load_music('background2.mp3')
        bgm.set_volume(22)
        bgm.repeat_play()
        play_mode.bgm2=True
def update():
    game_world.update()
    # delay(0.5)
def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
def finish():
    game_world.clear()
    pass
def pause():
    batter.wait_time=100000000000000000000000000000000.0
    pass
def resume():
    batter.wait_time=get_time()
    pass


