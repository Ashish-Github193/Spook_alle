import random
clock = 0
bgm = ["assets/sounds/bgm/bg1.wav", 
       "assets/sounds/bgm/bg2.wav", 
       "assets/sounds/bgm/bg3.wav", 
       "assets/sounds/bgm/bg4.wav" ]

torch = ["assets/sounds/torch/switch1.mp3",
         "assets/sounds/torch/switch2.wav",
         "assets/sounds/torch/hover2.mp3"]

wolf = ["assets/sounds/special/wolf2.wav",
        "assets/sounds/special/wolf3.wav",
        "assets/sounds/special/wolf4.wav",
        "assets/sounds/special/wolf5.wav"]

run_lis = ["assets/sounds/run/run1.wav", 
       "assets/sounds/run/run2.wav"]

walk = "assets/sounds/run/walk.wav"

blood_drip = 'assets/sounds/dead/blood_drip3.mp3'
spike_stab = "assets/sounds/dead/blood_drip.mp3"
trident_stab = "assets/sounds/dead/trident_stab.mp3"
impact = ['assets/sounds/impact/impact1.wav', 
          'assets/sounds/impact/impact2.wav']

soul_sound = 'assets/sounds/soul/soul_earn.wav'

def random_track(track_list):
   return random.choice(track_list)

def bytwofactor(track_list, clock):
    clock+=1
    if clock%2==0:
        return track_list[1]
    else:
        return track_list[0]