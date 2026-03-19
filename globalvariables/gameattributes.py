import constants

game_attributes = {"multiplier":1,
                   "player_type":"Circle",
                   "difficulty":1,
                   "player_ids": {},
                   "player": None,
                   "screen": None,
                   "width": constants.SCREEN_WIDTH,
                   "height": constants.SCREEN_HEIGHT}

combat_attributes = {"queue": [],
                   "queue_ids": {},
                   "enemy_count": 0,
                   "enemies": [],
                   "players": [],
                   "dead_enemies": [],
                   "dead_players": [],
                   "units": {},
                   "unit_turn": None,
                   "ability": None}

menus = {}