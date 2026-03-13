import sys

sys.path.append('.././globalvariables')

import pygame_menu as pm
import globalvariables.constants as constants
from globalvariables.gameattributes import game_attributes
from globalvariables.gameattributes import menus
import menucontroller

def create_player_menu(updatable, drawable):
    player_menu = pm.Menu(title="Player Menu",
                          onclose=pm.events.CLOSE,
                          menu_id="player_menu",
                          width = game_attributes["width"],
                          height = game_attributes["height"],
                          theme=pm.themes.THEME_DARK)
    
    player_menu.add.selector(title="Player Type\t",
                             items=constants.PLAYER_TYPES,
                             selector_id="player_type", 
                             onchange=menucontroller.select_player_type,
                             default=0)

    player_menu.add.selector(title="Difficulty\t",
                             items=constants.DIFFICULTY_LIST,
                             selector_id="difficulty", 
                             onchange=menucontroller.set_difficulty,
                             default=game_attributes["difficulty"])
    
    player_menu.add.button(title="Continue",
                           action=menucontroller.start_the_game,
                           accept_kwargs=True,
                           args=(updatable, drawable),
                           font_color=constants.WHITE, background_color=constants.GREEN,
                           align=pm.locals.ALIGN_CENTER)
    
    player_menu.add.button(title="Back",
                        action=pm.events.BACK,
                        font_color=constants.BLACK,
                        background_color=constants.RED,
                        align=pm.locals.ALIGN_CENTER)
    
    menus["player_menu"] = player_menu
    return player_menu