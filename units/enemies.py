import random
import math
import pygame

from globalvariables.constants import LINE_WIDTH as width
from globalvariables.gameattributes import combat_attributes
from units import Unit
import abilities as ability

class Enemy(Unit):
    def __init__(self, x, y, radius, multiplier, hero_level, targets):
        super().__init__(x, y, radius)
        self.set_attributes(multiplier, hero_level)
        self.xp_provided = (20 * self.level) * (self.level/hero_level)
        self.targets = targets
        self.abilities.append(ability.Ability("Sting", self.base_damage, 1.2, 1, False))
        self.type = "Star"

    def set_attributes(self, multiplier, hero_level):
        self.level = math.ceil(hero_level*(0.5*random.randint(1,2))*multiplier)
        self.initiative = random.randint(10+(self.level-1)+math.ceil(multiplier)-1, (10+(self.level-1)+math.floor(self.level*multiplier)+math.ceil(multiplier)))
        self.health = self.health + ((self.level-1)*(20*multiplier))
        self.base_damage = self.base_damage + ((self.level-1)*(1*multiplier))

    def star(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 45) * self.radius / 1.25
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        if not self.dead:
            pygame.draw.polygon(
            screen,
            "white",
            self.star(),
            width
            )
            self.draw_combat_attributes()
    
    def take_turn(self):
        random_action = random.randint(1,2)
        target = self.targets[random.randint(0, len(combat_attributes["players"])-1)]

        if random_action == 1:
            self.attack(target)
        else:
            if self.ability_points:
                ability_index = random.randint(0, len(self.abilities)-1)
                chosen_ability = self.abilities[ability_index]
                attempted_abilities = [ability_index]
                while chosen_ability.cost > self.ability_points:
                    while ability_index not in attempted_abilities:
                        ability_index = random.randint(0, len(self.abilities)-1)
                    chosen_ability = self.abilities[ability_index]
                    attempted_abilities.append(ability_index)
                self.use_ability(target, chosen_ability)
            else:
                self.attack(target)