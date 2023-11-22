from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time
from sdl2 import SDL_QUIT

import game_framework
import game_world

import play_mode
import state_variable
from attackplayer_topview import AtkPlayer
from ball_topview import Ball
#from outfielder_topview import Outfielder
from pitcher_topview import Pitcher


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
            # pitcher.handle_event(event)
            pass





def init():
    global image
    global logo_start_time
    global ball
    global atkplayer
    global pitcher
    global outfielder
    atkplayers = [AtkPlayer() for _ in range(state_variable.atkplayers_num)]
    for atkplayer in atkplayers:
        game_world.add_object(atkplayer, 1)
        # game_world.add_collision_pair('boy:ball', None, ball)
        # game_world.add_collision_pair('zombie:ball', None, ball)
    # atkplayer=AtkPlayer()
    # game_world.add_object(atkplayer, 1)
    pitcher = Pitcher()
    game_world.add_object(pitcher, 2)
    ball=Ball()
    game_world.add_object(ball, 2)
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