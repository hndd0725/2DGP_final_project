from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time
from sdl2 import SDL_QUIT

import game_framework
import game_world

import play_mode
import state_variable
from attackplayer_topview import AtkPlayer
from ball_topview import Ball
from outfielder_topview import Outfielder
#from outfielder_topview import Outfielder
from pitcher_topview import Pitcher


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            # pitcher.handle_event(event)
            pass

def init():
    global image
    global logo_start_time
    global ball
    global atkplayers
    global pitcher
    global outfielder
    atkplayers = [AtkPlayer(i) for i in range(0,100)]
    for i in range(0,state_variable.atkplayers_num):
        game_world.add_object(atkplayers[i], 1)
    #     # game_world.add_collision_pair('boy:ball', None, ball)
    #     # game_world.add_collision_pair('zombie:ball', None, ball)
    atkplayer=AtkPlayer(0)
    game_world.add_object(atkplayer, 2)

    outfielder=Outfielder()
    game_world.add_object(outfielder, 2)
    pitcher = Pitcher()
    game_world.add_object(pitcher, 0)
    ball=Ball()
    game_world.add_object(ball, 1)
    # outfielder=Outfielder()
    # game_world.add_object(outfielder, 2)

    image = load_image('SNES - Human Baseball JPN - Tokyo.png')
    pass
def finish():
    game_world.clear()
    pass
def update():
    game_world.update()

    pass
def draw():
    clear_canvas()
    image.draw(400,400)
    game_world.render()
    update_canvas()
    pass

def pause():
    pass
def resume():
    pass