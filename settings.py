import pygame, json


def get_save_data():
    with open("save_game/save_game.json", "r") as game_data:
        game_data = json.load(game_data)

    mist_ = game_data["mist"]
    sound = game_data["sound"]
    stage = game_data["stage"]
    name = game_data["name"]

    return [mist_, sound, stage, name]

def save_game_data(key, value):
    with open("save_game/save_game.json", "r") as game_data:
        data = json.load(game_data)
    data[key] = value
    with open("save_game/save_game.json", "w") as game_data:
        json.dump(data, game_data)


def save_leaderboard_temp_score(key, value):
    with open("save_game/leader_board_data.json", "r") as game_data:
        data = json.load(game_data)
    data[key][1] = value
    with open("save_game/leader_board_data.json", "w") as game_data:
        json.dump(data, game_data)


def save_leaderboard_final_score(key, value):
    with open("save_game/leader_board_data.json", "r") as game_data:
        data = json.load(game_data)
    data[key][0] += value
    data[key][1] = 0
    with open("save_game/leader_board_data.json", "w") as game_data:
        json.dump(data, game_data)


def get_leader_board_data():
    with open("save_game/leader_board_data.json", "r") as game_data:
        data = json.load(game_data)
    return data

def add_new_player_to_database(name):
    with open("save_game/leader_board_data.json", 'r') as game_data:
        data = json.load(game_data)
    data[name] = [0, 0]
    with open("save_game/leader_board_data.json", "w") as game_data:
        json.dump(data, game_data)



#---------------------- audio dependencies

#channel 0 is for bgm
#channel 1 is for wolf
#channel 2 is for player movement 
#channel 3 ghost
#channel 4 soul
#channel 5 blood and more deep elements
#channel 6 torch
#channel 7 player hurt
#channel 8 trident stab

channel0_volume = 0.05
channel1_volume = 0.02
channel2_volume = 0.2
channel3_volume = 0.1
channel4_volume = 0.1
channel5_volume = 0.1
channel6_volume = 0.5
channel7_volume = 0.5
channel8_volume = 0.1
channel9_volume = 1



#------------------------- settings dependencies



settings_in = True
r = False
s = False
a = False
played = False
resume_menu_play = [1, 1, 1, 1]
home_page_time = True
settings_click_time = [1, 1]
hover_home_screen = [0,0,0,0,0,0]
hover_home_play = [1,1,1,1,1,1]
click_home_screen = [1,1,1,1,1,1]
volume = bool(get_save_data()[1])
darkness = True
resume_menu = False


#--------- other items
