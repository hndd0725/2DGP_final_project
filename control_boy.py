from pico2d import *

import game_world
from grass import Grass
<<<<<<< HEAD
from batter import Batter
from pitcher import Pitcher
=======
from boy import Boy

>>>>>>> b1268b8fd92b7b43337f6f78e9264625113b4c53


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
<<<<<<< HEAD
            hitter.handle_event(event)
            pitcher.handle_event(event)
=======
            boy.handle_event(event)
>>>>>>> b1268b8fd92b7b43337f6f78e9264625113b4c53


def create_world():
    global running
    global grass
<<<<<<< HEAD
    global pitcher
    global hitter

    running = True

    hitter = Batter()
    game_world.add_object(hitter, 1)
    pitcher = Pitcher()
    game_world.add_object(pitcher, 1)
=======
    global team
    global boy

    running = True

    boy = Boy()
    game_world.add_object(boy,1)

>>>>>>> b1268b8fd92b7b43337f6f78e9264625113b4c53
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
<<<<<<< HEAD
    delay(0.3)
=======
    delay(0.01)
>>>>>>> b1268b8fd92b7b43337f6f78e9264625113b4c53
# finalization code
close_canvas()
