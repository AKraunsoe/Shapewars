
import pygame_menu as pm
import globalvariables.constants as constants
from globalvariables.gameattributes import game_attributes
from globalvariables.gameattributes import menus
import encounter.combatcontroller as combat

def create_combat_menu():
    combat_menu = pm.Menu(title="Combat",
                          width=game_attributes["width"],
                          height=game_attributes["height"]*(30/100),
                          enabled=False,
                          position=(0, 100),
                          menu_id="combat_menu",
                          theme=pm.themes.THEME_DARK)
    
    combat_menu.add.button(title="Attack",
                        action=combat.attack,
                        font_color=constants.BLACK,
                        background_color=constants.GREEN,
                        align=pm.locals.ALIGN_CENTER)
    
    combat_menu.add.button(title="Abilities",
                        action=combat.abilities,
                        font_color=constants.BLACK,
                        background_color=constants.BLUE,
                        align=pm.locals.ALIGN_CENTER)
    
    combat_menu.add.button(title="Items",
                        action=combat.items,
                        font_color=constants.WHITE,
                        background_color=constants.PURPLE,
                        align=pm.locals.ALIGN_CENTER)
    
    combat_menu.add.button(title="Flee",
                        action=combat.flee,
                        font_color=constants.BLACK,
                        background_color=constants.RED,
                        align=pm.locals.ALIGN_CENTER)
    

    menus["combat_menu"] = combat_menu
    return combat_menu