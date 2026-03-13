import sys

sys.path.append('.././globalvariables')

import pygame_menu as pm
import globalvariables.constants as constants
from globalvariables.gameattributes import game_attributes
from globalvariables.gameattributes import menus

def CreateCombatMenu():
    combat_menu = pm.Menu(title="Combat",
                          width=game_attributes["width"],
                          height=game_attributes["height"]*(30/100),
                          enabled=False,
                          position=(0, 0),
                          menu_id="combat_menu",
                          theme=pm.themes.THEME_DARK)
    
    
    menus["combat_menu"] = combat_menu
    return combat_menu