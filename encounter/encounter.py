import pygame
import pygame_menu as pm

from globalvariables.gameattributes import combat_attributes, game_attributes, menus, constants

def encounter(players, enemies):
    units = players + enemies
    sorted(units, key=lambda unit: unit.initiative)
    combat_units = combat_attributes["units"] or {}
    combat_attributes["players"] = players
    combat_attributes["enemies"] = enemies
    combat_attributes["enemy_count"] = len(enemies)
    for unit in units:
        if unit.id not in combat_units:
            combat_units[unit.id] = unit
    combat_attributes["units"] = combat_units
    update_queue()
    add_player_abilities(players)
    menus["combat_menu"].enable()


def add_to_queue(units):
    queue = combat_attributes["queue"] or []
    ids = combat_attributes["queue_ids"] or {}
    while len(queue) < 8:
        added = False
        if len(queue) == 0:
            queue.append(units[0])
            ids[units[0].id] = 1
            units[0].turn = True
            combat_attributes["unit_turn"] = units[0]   
        else:
            highest_initiative = float("-inf")
            best_unit = None
            for unit in units:
                if unit.dead:
                    continue
                elif unit.id in ids:
                    new_initiative = unit.initiative-(5*ids[unit.id])
                    highest_initiative = max(new_initiative, highest_initiative)
                    best_unit = unit if new_initiative == highest_initiative else best_unit
                elif unit.initiative >= highest_initiative:
                    highest_initiative = unit.initiative
                    best_unit = unit
                elif best_unit:
                    queue.append(best_unit)
                    if best_unit.id in ids:
                        ids[best_unit.id] += 1
                    else:
                        ids[best_unit.id] = 1
                    added = True
                    break
                else:
                    raise Exception(f"Error creating queue, highest_ini:{highest_initiative}\nbest_uni:{best_unit}\nqueue:{queue}\nids:{ids}")
            if not added:
                queue.append(best_unit)
                if best_unit.id in ids:
                    ids[best_unit.id] += 1
                else:
                    ids[best_unit.id] = 1

    combat_attributes["queue"] = queue
    combat_attributes["queue_ids"] = ids

def draw_queue():
    queue = combat_attributes["queue"]
    if len(queue) >0:
        font = pygame.font.SysFont('calibri', 25)

        for i in range(len(queue)):
            unit = queue[i]
            text = font.render(str(f"{unit.level} {unit.type} {unit.health}"), True, constants.WHITE)
            queue_position = pygame.Vector2(0,0+(i*33))
            game_attributes["screen"].blit(text, queue_position)
    

def update_queue():
    queue = combat_attributes["queue"]
    units = list(combat_attributes["units"].values())
    dead_players = combat_attributes["dead_players"]
    dead_enemies = combat_attributes["dead_enemies"]
    if len(queue) > 0:
        queue.pop(0)

        for i in range(len(queue)-1, -1, -1):
            if queue[i].dead:
                queue.pop(i)
        
        queue[0].turn = True

        combat_attributes["unit_turn"] = queue[0]
    
        for j in range(len(units)-1, -1, -1):
            unit = units[j]
            if unit.dead:
                if unit.player:
                    dead_players.append(unit)
                else:
                    dead_enemies.append(unit)
                del combat_attributes["units"][unit.id]

        print(f"dead_enemies: {dead_enemies}\nenemies: {combat_attributes["enemies"]}\ndead_players: {dead_players}\nplayers: {combat_attributes["players"]}")

    if (len(dead_enemies) == len(combat_attributes["enemies"]) or
        len(dead_players) == len(combat_attributes["players"])) and len(combat_attributes["players"])> 0:
        end_encounter(*(), **{'kwargs': (combat_attributes["players"], combat_attributes["dead_enemies"], combat_attributes["enemies"])})
    else:
        combat_attributes["queue"] = queue

        add_to_queue(units)
        draw_queue()
        show_buttons(*(),**{'args': ("main")})

def attack(*args, **kwargs):
    print(f"{args}, {kwargs}")
    if 'args' not in kwargs:
        raise Exception("no args given for attack")
    index = kwargs['args']
    enemies = combat_attributes["enemies"]
    if index >= len(enemies):
        index = len(enemies)-1
    target = enemies[index]
    
    ability = combat_attributes["ability"]
    print(f"ability: {ability}")
    if ability:
        combat_attributes["unit_turn"].use_ability(target, ability)
    else:
        combat_attributes["unit_turn"].attack(target)


def end_encounter(*args, **kwargs):

    print(f"end encounter:{kwargs}\n{args}")

    players = combat_attributes["players"]
    if len(players):
        dead_enemies = combat_attributes["dead_enemies"]
        enemies = combat_attributes["enemies"]

        xp_gained = 0

        for dead_enemy in dead_enemies:
            xp_gained+=dead_enemy.xp_provided

        for enemy in enemies:
            del game_attributes["player_ids"][enemy.id]
            enemy.kill()
        
        for player in players:
            player.post_encounter(xp_gained)

        combat_attributes["queue"] = []
        combat_attributes["queue_ids"] = {}
        combat_attributes["enemy_count"] = 0
        combat_attributes["enemies"] = []
        combat_attributes["players"] = []
        combat_attributes["dead_enemies"] = []
        combat_attributes["dead_players"] = []
        combat_attributes["units"] = {}
        combat_attributes["unit_turn"] = None
        combat_attributes["ability"] = None
        
        show_buttons(*(),**{'args': ("main")})

        menus["combat_menu"].disable()

def add_player_abilities(players):
    combat_menu = menus['combat_menu']
    for i in range(len(players)):
        player = players[i]
        for j in range(len(player.abilities)):
            widget = combat_menu.get_widget(f"{player.type}_ability_{j}")
            if not widget:
                combat_menu.add.button(title=f"{player.abilities[j].name} {player.abilities[j].cost}",
                                       button_id=f"{player.type}_ability_{j}",
                                       action=show_buttons,
                                       accept_kwargs=True,
                                       args=("target", player.abilities[j]),
                                       font_color=constants.BLACK,
                                       background_color=constants.BLUE,
                                       align=pm.locals.ALIGN_CENTER)
                combat_menu.get_widget(f"{player.type}_ability_{j}").hide()
            else:
                widget.hide()
    menus['combat_menu'] = combat_menu

def show_buttons(*args, **kwargs):
    print(f"buttons: {args}\n{kwargs}")
    if 'args' not in kwargs:
        raise Exception("missing args to show buttons")
    type = kwargs['args'] if isinstance(kwargs['args'], str) else kwargs['args'][0]
    player = combat_attributes["unit_turn"]
    character_type = player.type if player else None
    ability = kwargs['args'][1] if not isinstance(kwargs['args'], str) and len(kwargs['args']) >= 2 else None
    combat_attributes["ability"] = ability

    if ability and not (player.ability_points >= ability.cost):
        type = "main"

    main_buttons = ["attack", "abilities", "flee"]
    target_buttons = ["left", "right", "middle"]
    ability_butttons = f"{character_type}_ability_"

    widgets = menus["combat_menu"].get_widgets()
    print(f"type:{type}")
    for widget in widgets:
        match type:
            case "main":
                if widget.get_id() in main_buttons:
                    widget.show()
                else:
                    widget.hide()
            case "target":
                enemies_count = combat_attributes["enemy_count"]
                
                if widget.get_id() in target_buttons:
                    if enemies_count == 3:
                        widget.show()
                    elif enemies_count == 2 and widget.get_id() != "middle":
                        widget.show()
                    elif enemies_count == 1 and widget.get_id() == "middle":
                        widget.show()
                else:
                    widget.hide()
            case "ability":
                print(f"widget: {widget.get_id()}")
                print(f"ability_button: {ability_butttons}")
                if ability_butttons in widget.get_id():
                    widget.show()
                else:
                    widget.hide()
