import sys

sys.path.append('.././globalvariables')

import pygame_menu as pm
import globalvariables.constants as constants
from globalvariables.gameattributes import game_attributes
from globalvariables.gameattributes import menus
import menucontroller


def CreateSettingsMenu():
    settings = pm.Menu(title = "Settings",
                       menu_id="settings",
                       width = game_attributes["width"],
                       height = game_attributes["height"],
                       theme = pm.themes.THEME_DARK)
    
    settings._theme.widget_font_size = 25
    settings._theme.widget_font_color = constants.WHITE
    settings._theme.widget_alignment = pm.locals.ALIGN_LEFT


    settings.add.dropselect(title="Window Resolution",
                            items=constants.RESOLUTION,
                            dropselect_id="resolution",
                            open_middle=True,
                            selection_box_height=6,
                            onchange=menucontroller.set_resolution,
                            default=3)
    
    settings.add.clock(clock_format="%d-%m-%y %H:%M:%S",
                       title_format="Local Time: {0}")

    settings.add.selector(title="Difficulty\t",
                             items=constants.DIFFICULTY_LIST,
                             selector_id="difficulty_settings", 
                             onchange=menucontroller.set_difficulty,
                             default=game_attributes["difficulty"])

    settings.add.button(title="Back to Main Menu",
                        action=pm.events.BACK,
                        font_color=constants.BLACK,
                        background_color=constants.WHITE,
                        align=pm.locals.ALIGN_CENTER)
    
    menus["settings"] = settings
    return settings