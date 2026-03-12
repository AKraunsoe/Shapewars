import sys

sys.path.append('./units') 

import pygame
import pygame_menu as pm
import constants
from units import Player

# Standard RGB colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 100, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def main():
    pygame.init()
    pygame.display.set_caption("Window using Pygame_menu")
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

    game_attributes = {"multiplier":1,
                       "player_type":"Circle",
                       "difficulty":1,
                       "width": constants.SCREEN_WIDTH,
                       "height": constants.SCREEN_HEIGHT}

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    clock = pygame.time.Clock()
    dt = 0

    resolution = [("1920x1080", "1920x1080"),
                  ("1920x1200", "1920x1200"),
                  ("1600x900", "1600x900"),
                  ("1280x720", "1280x720"),
                  ("800x600", "800x600")]
    
    difficultyList = [("Easy", "Easy"),
                  ("Normal", "Normal"),
                  ("Hard", "Hard"),
                  ("Impossible", "Impossible")]
    
    types = [("Circle", "Circle"),
             ("Triangle", "Triangle"),
             ("Square", "Square")]
    
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
        player_menu.disable()
        settings.disable()
        main_menu.disable()  
    
    def set_resolution(*args, **kwargs):
        value = args[0]
        print(f"tested {value}")
        if len(value[0]) > 0:
            width, height = value[0][0].split("x")
            pygame.display.set_mode((int(width), int(height)))
            settings.get_widget("resolution").set_value(value[0][0])
            settings.get_widget("resolution").placeholder = value[0][0]
            main_menu.resize(int(width), int(height))
            settings.resize(int(width), int(height))
            player_menu.resize(int(width), int(height))
            game_attributes["width"] = width
            game_attributes["height"] = height

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
    
    settings = pm.Menu(title = "Settings",
                       width = game_attributes["width"],
                       height = game_attributes["height"],
                       theme = pm.themes.THEME_DARK)
    
    settings._theme.widget_font_size = 25
    settings._theme.widget_font_color = WHITE
    settings._theme.widget_alignment = pm.locals.ALIGN_LEFT

    #settings.add.text_input(title="User Name: ", textinput_id="username")

    settings.add.dropselect(title="Window Resolution",
                            items=resolution,
                            dropselect_id="resolution",
                            open_middle=True,
                            selection_box_height=6,
                            onchange=set_resolution,
                            default=3)
    
    settings.add.clock(clock_format="%d-%m-%y %H:%M:%S",
                       title_format="Local Time: {0}")
    """
    settings.add.button(title="Restore Defaults",
                        action=settings.reset_value,
                        font_color=WHITE, background_color=RED)

    """

    settings.add.selector(title="Difficulty\t",
                             items=difficultyList,
                             selector_id="difficulty_settings", 
                             onchange=set_difficulty,
                             default=game_attributes["difficulty"])

    settings.add.button(title="Back to Main Menu",
                        action=pm.events.BACK,
                        font_color=BLACK,
                        background_color=WHITE,
                        align=pm.locals.ALIGN_CENTER)

    player_menu = pm.Menu(title="Player Menu",
                          onclose=pm.events.CLOSE,
                          width = game_attributes["width"],
                          height = game_attributes["height"],
                          theme=pm.themes.THEME_DARK)
    
    player_menu.add.selector(title="Player Type\t",
                             items=types,
                             selector_id="player_type", 
                             onchange=select_player_type,
                             default=0)

    player_menu.add.selector(title="Difficulty\t",
                             items=difficultyList,
                             selector_id="difficulty", 
                             onchange=set_difficulty,
                             default=game_attributes["difficulty"])
    
    player_menu.add.button(title="Continue",
                           action=start_the_game,
                           accept_kwargs=True,
                           args=(updatable, drawable),
                           font_color=WHITE, background_color=GREEN,
                           align=pm.locals.ALIGN_CENTER)
    
    player_menu.add.button(title="Back",
                        action=pm.events.BACK,
                        font_color=BLACK,
                        background_color=RED,
                        align=pm.locals.ALIGN_CENTER)

    main_menu = pm.Menu(title="Main Menu",
                        width=game_attributes["width"],
                        height=game_attributes["height"],
                        enabled=True,
                        center_content=True,
                        menu_id="main_menu",
                        theme=pm.themes.THEME_DARK)
    
    main_menu.add.button(title="Play", action=player_menu,
                         font_color=WHITE, background_color=GREEN,
                         align=pm.locals.ALIGN_CENTER)
    main_menu.add.button(title="Settings", action=settings,
                         font_color=WHITE, background_color=CYAN,
                         align=pm.locals.ALIGN_CENTER)
    main_menu.add.button(title="Exit", action=pm.events.EXIT,
                         font_color=WHITE, background_color=RED,
                         align=pm.locals.ALIGN_CENTER)


    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu.enable()
            
        if main_menu.is_enabled():
            main_menu.draw(screen)
            main_menu.update(events)            
        elif settings.is_enabled():
            settings.draw(screen)
            settings.update(events)
        elif player_menu.is_enabled():
            player_menu.draw(screen)
            player_menu.update(events)
        else:
            screen.fill("black")
            for dable in drawable:
                dable.draw(screen, game_attributes["player_type"])
            pygame.display.flip()
            dt = clock.tick(60) /1000
            updatable.update(dt)
            
        pygame.display.update()


if __name__ == "__main__":
    main()
