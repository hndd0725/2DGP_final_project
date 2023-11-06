from pico2d import *

import batter
import game_world

from batter import Batter
from grass import Grass
import game_framework
from pitcher import Pitcher


# Game object class here


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


    grass = Grass()
    game_world.add_object(grass, 0)

    batter = Batter()
    game_world.add_object(batter, 2)
    pitcher = Pitcher()
    game_world.add_object(pitcher, 2)

def update():
    game_world.update()


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


# def create_world():
#     global running
#     global grass
#     global pitcher
#     global hitter
#
#     running = True
#
#     hitter = Batter()
#     game_world.add_object(hitter, 2)
#     pitcher = Pitcher()
#     game_world.add_object(pitcher, 2)
#
#     running = True
#
#
#     grass = Grass()
#     game_world.add_object(grass, 0)