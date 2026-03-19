
import uuid
import pygame

from circleshape import CircleShape

from globalvariables.gameattributes import game_attributes, combat_attributes, constants
from encounter import update_queue


class Unit(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = 0
        self.initiative = 10
        self.health = 100
        self.ability_points = 0
        self.base_damage = 10
        self.abilities = []
        self.level = 1
        self.type = None
        self.player = False
        self.id = self.create_id()
        self.turn = False
        self.dead = False

    def create_id(self):
        id = uuid.uuid4().int
        while id in game_attributes["player_ids"]:
            id = uuid.uuid4().int
        game_attributes["player_ids"][id] =1
        return id
    
    def attack(self, target):
        target.health -= self.base_damage
        if target.health <=0:
            target.dead = True
        self.ability_points +=1
        if self.turn:
            self.turn = False
            update_queue()

    def use_ability(self, target, selected_ability):
        if selected_ability.multi_target:
            pass
        else:
            target.health -= selected_ability.damage
            if target.health <=0:
                target.dead = True
        self.ability_points -= selected_ability.cost
        self.ability_points += selected_ability.generate
        if self.turn:
            self.turn = False
            update_queue()
    
    def draw_combat_attributes(self):
        font = pygame.font.SysFont('calibri', 15)

        hp = font.render(str(self.health), True, constants.WHITE)
        hp_pos = pygame.Vector2(self.position.x-15, self.position.y+(self.radius*1.5))

        level = font.render(str(self.level), True, constants.WHITE)
        level_pos = pygame.Vector2(self.position.x-(self.radius*1.4), self.position.y)

        action_points = font.render(str(f"AP: {self.ability_points}"), True, constants.WHITE)
        action_points_position = pygame.Vector2(self.position.x+(self.radius*1.2), self.position.y)

        game_attributes["screen"].blit(hp, hp_pos)
        game_attributes["screen"].blit(level, level_pos)
        game_attributes["screen"].blit(action_points, action_points_position)