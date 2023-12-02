from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time, load_font, load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE
import game_framework
import play_mode


def init():
    global image
    global logo_start_time
    global bgm
    image = load_image('baseball_title.jpg')
    bgm = load_music('title_sound.mp3')
    bgm.set_volume(50)
    bgm.repeat_play()
    pass
def finish():
    pass
def update():
        pass
def draw():
    clear_canvas()
    image.draw(400,300,800,600)
    load_font('ENCR10B.TTF', 45).draw(150, 300, "Press the space bar", (255, 0, 255))
    update_canvas()
    pass
def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            bgm.stop()
            game_framework.change_mode(play_mode)


def pause():
    pass

def pause():
    pass
def resume():
    pass