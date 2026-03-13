

import pygame_menu as pm
import pygame
import globalvariables.constants as constants
from globalvariables.gameattributes import game_attributes
from globalvariables.gameattributes import menus
from units import Player

def get_main_menu():
    if "main_menu" in menus:
        main_menu = menus["main_menu"]

        if not main_menu:
            raise Exception(f"Missing main menu={main_menu}")
        
        return main_menu
    return None

def get_settings_menu():
    if "settings" in menus:
        settings = menus["settings"]

        if not settings:
            raise Exception(f"Missing settings menu={settings}")
        
        return settings
    return None
    
def get_player_menu():
    if "player_menu" in menus:
        player_menu = menus["player_menu"]

        if not player_menu:
            raise Exception(f"Missing player menu={player_menu}")
        
        return player_menu
    return None

def set_resolution(*args, **kwargs):
    value = args[0]
    print(f"tested {value}")
    if len(value[0]) > 0:
        width, height = value[0][0].split("x")
        pygame.display.set_mode((int(width), int(height)))
        settings = get_settings_menu()
        main_menu = get_main_menu()
        player_menu = get_player_menu()

        if settings:       
            settings.get_widget("resolution").set_value(value[0][0])
            settings.get_widget("resolution").placeholder = value[0][0]
            settings.resize(int(width), int(height))
        
        if main_menu:
            main_menu.resize(int(width), int(height))
        
        if player_menu:
            player_menu.resize(int(width), int(height))

        game_attributes["width"] = int(width)
        game_attributes["height"] = int(height)

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

    settings = get_settings_menu()
    main_menu = get_main_menu()
    player_menu = get_player_menu()

    settings.disable()
    main_menu.disable()
    player_menu.disable()  
     

def set_difficulty(*args, **kwargs):
    value = args[0]
    settings = get_settings_menu()
    player_menu = get_player_menu()
    print(f"difficulty {value}")
    if len(value[0]) > 0:
        i_type = value[0][0]
        match i_type:
            case "Easy":
                game_attributes["difficulty"] = 0
                game_attributes["multiplier"] = 0.5
                if settings:
                    settings.get_widget("difficulty").set_value(0)
                if player_menu:
                    player_menu.get_widget("difficulty").set_value(0)
            case "Normal":
                game_attributes["difficulty"] = 1
                game_attributes["multiplier"] = 1
                if settings:
                    settings.get_widget("difficulty").set_value(1)
                if player_menu:
                    player_menu.get_widget("difficulty").set_value(1)
            case "Hard":
                game_attributes["difficulty"] = 2
                game_attributes["multiplier"] = 2
                if settings:
                    settings.get_widget("difficulty").set_value(2)
                if player_menu:
                    player_menu.get_widget("difficulty").set_value(2)
            case "Impossible":
                game_attributes["difficulty"] = 3
                game_attributes["multiplier"] = 5
                if settings:
                    settings.get_widget("difficulty").set_value(3)
                if player_menu:
                    player_menu.get_widget("difficulty").set_value(3)

def select_player_type(*args, **kwargs):
    value = args[0]
    print(f"player type {value}")
    if len(value[0]) > 0:
        
        game_attributes["player_type"] = value[0][0]