
import pygame
from globalvariables.gameattributes import game_attributes, combat_attributes
import Menus.combatmenu as combatmenu
import Menus.settingsmenu as settingsmenu
import Menus.mainmenu as mainmenu
import Menus.playermenu as playermenu

def game():
    pygame.init()
    pygame.display.set_caption("Window using Pygame_menu")
    screen = pygame.display.set_mode((game_attributes["width"], game_attributes["height"]))
    combat_rect = pygame.Rect(0, 0, game_attributes["width"], game_attributes["height"]*7/10)
    game_attributes["screen"] = screen
    game_attributes["combat_screen"] = combat_rect

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    clock = pygame.time.Clock()
    dt = 0

    settings = settingsmenu.create_settings_menu()
    player_menu = playermenu.create_player_menu(updatable, drawable)
    main_menu = mainmenu.create_main_menu()
    combat_menu = combatmenu.create_combat_menu()

    combat_menu_buttons = [pygame.K_w, pygame.K_UP, pygame.K_a,
                           pygame.K_LEFT, pygame.K_s, pygame.K_d, 
                           pygame.K_DOWN, pygame.K_RIGHT, pygame.K_KP_ENTER]

    while True:
        events = pygame.event.get()
        player_turn = combat_attributes["unit_turn"].player if combat_attributes["unit_turn"] else None
        for event in events:
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu.enable()
            if  event.type == pygame.KEYDOWN and combat_menu.is_enabled() and player_turn and event.key in combat_menu_buttons:
                key = event.key
                if key == pygame.K_KP_ENTER:
                    combat_menu.get_selected_widget()._onreturn
                else:
                    widgets = combat_menu.get_widgets()
                    print(len(widgets))
                    previous = None
                    next = None
                    for i in range(len(widgets)):
                        if widgets[i].is_selected():
                            widgets[i].select(False)
                            if i == 0:
                                previous = len(widgets)-1
                                next = i+1
                                break
                            elif i == len(widgets)-1:
                                previous = i-1
                                next = 0
                                break
                            else:
                                previous = i-1
                                next = i+1
                                break
                    if key == pygame.K_w or key==pygame.K_a or key==pygame.K_LEFT:
                        print(f"widget selected: {widgets[previous].get_id()}")
                        combat_menu.get_widget(widgets[previous].get_id()).select()
                    elif key==pygame.K_s or key==pygame.K_d or key==pygame.K_RIGHT:
                        print(f"widget selected: {widgets[next].get_id()}")
                        combat_menu.get_widget(widgets[next].get_id()).select()        
            
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
            """
            for menu in menus:
                if menu in enabled_menus:
                    enabled_menus[menu].disable()
                    del enabled_menus[menu]
            """

            if combat_menu.is_enabled():
                combat_menu.draw(screen)
                combat_menu.update(events)
                screen.fill("black", game_attributes["combat_screen"])
            else:
                screen.fill("black")

            for dable in drawable:
                dable.draw(screen)
            pygame.display.flip()
            dt = clock.tick(60) /1000
            updatable.update(dt)
            

            if not player_turn and player_turn is not None:
                combat_attributes["unit_turn"].take_turn()
            
            
            
        pygame.display.update()