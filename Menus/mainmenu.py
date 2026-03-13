import sys

sys.path.append('.././globalvariables')
sys.path.append('.././units')

import pygame_menu as pm
import globalvariables.constants as constants
from globalvariables.gameattributes import game_attributes
from globalvariables.gameattributes import menus

def create_main_menu():
    main_menu = pm.Menu(title="Main Menu",
                        width=game_attributes["width"],
                        height=game_attributes["height"],
                        enabled=True,
                        center_content=True,
                        menu_id="main_menu",
                        theme=pm.themes.THEME_DARK)
    
    main_menu.add.button(title="Play", action=menus["player_menu"],
                         font_color=constants.WHITE, background_color=constants.GREEN,
                         align=pm.locals.ALIGN_CENTER)
    main_menu.add.button(title="Settings", action=menus["settings"],
                         font_color=constants.WHITE, background_color=constants.CYAN,
                         align=pm.locals.ALIGN_CENTER)
    main_menu.add.button(title="Exit", action=pm.events.EXIT,
                         font_color=constants.WHITE, background_color=constants.RED,
                         align=pm.locals.ALIGN_CENTER)
    
    menus["main_menu"] = main_menu
    return main_menu