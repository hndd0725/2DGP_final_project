from pico2d import *

import game_world
from grass import Grass
from batter import Batter
from pitcher import Pitcher


# Game object class here


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            hitter.handle_event(event)
            pitcher.handle_event(event)



def create_world():
    global running
    global grass
    global pitcher
    global hitter

    running = True

    hitter = Batter()
    game_world.add_object(hitter, 1)
    pitcher = Pitcher()
    game_world.add_object(pitcher, 1)


    running = True


    grass = Grass()
    game_world.add_object(grass, 0)




def update_world():
   game_world.update()


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()


open_canvas(800,600)
create_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
