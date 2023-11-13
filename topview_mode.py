from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time
from sdl2 import SDL_QUIT

import game_framework
import game_world
import pitcher
import play_mode
from pitcher import Pitcher


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
    global pitchar
    pitcher = Pitcher()
    game_world.add_object(pitcher, 2)
    logo_start_time=get_time()
    image = load_image('SNES - Human Baseball JPN - Tokyo.png')
    pass
def finish():
    game_world.clear()
    pass
def update():
    game_world.update()
    # if get_time()-logo_start_time>=2.0:
    #     game_framework.change_mode(play_mode)
    pass
def draw():
    clear_canvas()
    image.draw(400,300)
    game_world.render()
    update_canvas()
    pass

def pause():
    pass
def resume():
    pass