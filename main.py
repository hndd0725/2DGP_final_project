from pico2d import open_canvas, delay, close_canvas
import game_framework
#import play_mode as start_mode
#import topview_mode as start_mode
import logo_mode as start_mode
#import title_mode as start_mode
#import lose_mode as start_mode


open_canvas()
game_framework.run(start_mode)
close_canvas()
