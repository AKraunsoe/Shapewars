import sys

sys.path.append('./Menus')
sys.path.append('./globalvariables')


import pygame
import pygame_menu as pm
import globalvariables.constants as constants
import globalvariables.gameattributes as game_attributes
import Menus.combatmenu as combatmenu
import Menus.settingsmenu as settingsmenu
import Menus.mainmenu as mainmenu
import Menus.playermenu as playermenu

# Standard RGB colors


def main():
    pygame.init()
    pygame.display.set_caption("Window using Pygame_menu")
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    clock = pygame.time.Clock()
    dt = 0

    settings = settingsmenu.CreateSettingsMenu()
    player_menu = playermenu.CreatePlayerMenu(updatable, drawable)
    main_menu = mainmenu.CreateMainMenu(player_menu, settings)
    
    combat_menu = combatmenu.CreateCombatMenu()

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
        elif game_attributes["player"].encounter_chance >= 100:
            if combat_menu.is_enabled():
                combat_menu.draw(screen)
                combat_menu.update(events)
            else:
                combat_menu.enable()
        else:
            screen.fill("black")
            for dable in drawable:
                dable.draw(screen, game_attributes["player_type"])
            pygame.display.flip()
            dt = clock.tick(60) /1000
            updatable.update(dt, game_attributes)
            
        pygame.display.update()


if __name__ == "__main__":
    main()
