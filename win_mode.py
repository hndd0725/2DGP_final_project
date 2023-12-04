from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time, load_font, load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDLK_r
import game_framework
import play_mode
import state_variable


def init():
    global image
    global logo_start_time
    image = load_image('win.jpg')
    pass
def finish():
    pass
def update():
        pass
def draw():
    clear_canvas()
    image.draw(400,300,800,600)
    load_font('ENCR10B.TTF', 45).draw(55, 50, "my_point: " f'{state_variable.my_point}', (0, 255, 255))
    load_font('ENCR10B.TTF', 45).draw(400, 50, "other_point: " f'{state_variable.other_point}', (255, 0, 0))

    if get_time()%2<1:
        load_font('ENCR10B.TTF', 45).draw(150, 300, "Press the space R", (255, 0, 255))
    update_canvas()
    pass
def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_r):
            state_variable.atkplayerBase_num = 0
            state_variable.atkplayers_num = 0
            state_variable.atk_loc = [0 for _ in range(0, 100)]
            state_variable.atk_life = [0 for _ in range(0, 100)]
            state_variable.ball_catch = False
            state_variable.logo_start_time = 100000000000000000
            state_variable.strike_num = 0
            state_variable.ball_num = 0
            state_variable.three_out = 0
            state_variable.atk_safe = False
            state_variable.my_point = 0
            state_variable.other_point = 0
            state_variable.state_4ball = False
            state_variable.is_swing_more_one = 0
            state_variable.game_num = 0
            game_framework.change_mode(play_mode)


def pause():
    pass

def pause():
    pass
def resume():
    pass