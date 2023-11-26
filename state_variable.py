import random

swing=False
hit_ballend_x = random.randint(80, 550)
hit_ballend_y =random.randint(400, 600)#홈런이 아닐때
atkplayerStart_x,atkplayerStart_y= 400, -30#홈400-30
atkplayerEnd_x,atkplayerEnd_y= 490, 50#1루490,50
atkplayerBase_num=0
atkplayers_num=0
atk_loc = [0 for _ in range(0,100)]
ball_catch=False
logo_start_time=100000000000000000
strike_num=0
ball_num=0
