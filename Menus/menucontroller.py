import sys

sys.path.append('.././globalvariables')
sys.path.append('.././units')

import pygame_menu as pm
import pygame
import globalvariables.constants as constants
from globalvariables.gameattributes import game_attributes
from globalvariables.gameattributes import menus
from units.units import Player

def set_resolution(*args, **kwargs):
    value = args[0]
    print(f"tested {value}")
    if len(value[0]) > 0:
        width, height = value[0][0].split("x")
        pygame.display.set_mode((int(width), int(height)))
        settings = menus["settings"]
        main_menu = menus["main_menu"]
        player_menu = menus["player_menu"]

        if not settings or not main_menu or not player_menu:
            raise Exception(f"Missing options menu for resolution change settings={settings}\nmainmenu={main_menu}\nplayer_menu={player_menu}")

        settings.get_widget("resolution").set_value(value[0][0])
        settings.get_widget("resolution").placeholder = value[0][0]
        main_menu.resize(int(width), int(height))
        settings.resize(int(width), int(height))
        player_menu.resize(int(width), int(height))
        game_attributes["width"] = width
        game_attributes["height"] = height

def start_the_game(*args, **kwargs):
    print("start the game")

    print(game_attributes)
    print(kwargs)
    if 'args' not in kwargs:
        print("no args")
        pygame.quit

    game_args = kwargs['args']     
        
    #updatable, drawable
    Player.containers = (game_args[0], game_args[1])

    player = Player(game_attributes["width"] / 2, game_attributes["height"] / 2, constants.PLAYER_RADIUS)
    game_attributes["player"] = player    
    pm.Menu.get_id("settings").disable()
    pm.Menu.get_id("main_menu").disable()
    pm.Menu.get_id("player_menu").disable()  
     

def set_difficulty(*args, **kwargs):
    value = args[0]
    print(f"difficulty {value}")
    if len(value[0]) > 0:
        i_type = value[0][0]
        match i_type:
            case "Easy":
                game_attributes["difficulty"] = 0
                game_attributes["multiplier"] = 0.5
            case "Normal":
                game_attributes["difficulty"] = 1
                game_attributes["multiplier"] = 1
            case "Hard":
                game_attributes["difficulty"] = 2
                game_attributes["multiplier"] = 2
            case "Impossible":
                game_attributes["difficulty"] = 3
                game_attributes["multiplier"] = 5

def select_player_type(*args, **kwargs):
    value = args[0]
    print(f"player type {value}")
    if len(value[0]) > 0:
        
        game_attributes["player_type"] = value[0][0]