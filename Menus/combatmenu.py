
import pygame_menu as pm
import globalvariables.constants as constants
from globalvariables.gameattributes import game_attributes, combat_attributes
from globalvariables.gameattributes import menus
from encounter import attack, end_encounter, show_buttons

def create_combat_menu():
    combat_menu = pm.Menu(title="Combat",
                          width=game_attributes["width"],
                          height=game_attributes["height"]*(30/100),
                          enabled=False,
                          position=(0, 100),
                          menu_id="combat_menu",
                          theme=pm.themes.THEME_DARK)
    
    combat_menu.add.button(title="Attack",
                           button_id="attack",
                           action=show_buttons,
                           accept_kwargs=True,
                           args=("target"),
                           font_color=constants.BLACK,
                           background_color=constants.GREEN,
                           align=pm.locals.ALIGN_CENTER)
    
    combat_menu.add.button(title="Abilities",
                           button_id="abilities",
                           action=show_buttons,
                           accept_kwargs=True,
                           args=("ability"),
                           font_color=constants.BLACK,
                           background_color=constants.BLUE,
                           align=pm.locals.ALIGN_CENTER)
    """
    combat_menu.add.button(title="Items",
                           button_id="items",
                           action=combat.items,
                           font_color=constants.WHITE,
                           background_color=constants.PURPLE,
                           align=pm.locals.ALIGN_CENTER)
    """     
    
    combat_menu.add.button(title="Flee",
                           button_id="flee",
                           action=end_encounter,
                           font_color=constants.BLACK,
                           background_color=constants.RED,
                           align=pm.locals.ALIGN_CENTER)

    combat_menu.add.button(title="Left",
                           button_id="left",
                           action=attack,
                           accept_kwargs=True,
                           args=(0),
                           font_color=constants.BLACK,
                           background_color=constants.GREEN,
                           align=pm.locals.ALIGN_LEFT
                           )
   
    combat_menu.add.button(title="Middle",
                           button_id="middle",
                           action=attack,
                           accept_kwargs=True,
                           args=(1),
                           font_color=constants.BLACK,
                           background_color=constants.BLUE,
                           align=pm.locals.ALIGN_CENTER
                           )
    combat_menu.add.button(title="Right",
                           button_id="right",
                           action=attack,
                           accept_kwargs=True,
                           args=(2),
                           font_color=constants.BLACK,
                           background_color=constants.RED,
                           align=pm.locals.ALIGN_RIGHT
                           )
    
    combat_menu.get_widget("left").hide()
    combat_menu.get_widget("middle").hide()
    combat_menu.get_widget("right").hide()
    
    menus["combat_menu"] = combat_menu
    return combat_menu


