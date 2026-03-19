
import random
import math
import pygame

from encounter import encounter, draw_queue
from units import Unit
from enemies import Enemy
from globalvariables.constants import LINE_WIDTH as width
from globalvariables.constants import PLAYER_TURN_SPEED as turn_speed
from globalvariables.constants import PLAYER_SPEED as speed
from globalvariables.constants import PLAYER_RADIUS as p_radius
from globalvariables.gameattributes import game_attributes, combat_attributes
import abilities as ability

class Player(Unit):
    def __init__(self, x, y, radius, main):
        super().__init__(x, y, radius)
        self.encounter_chance = 0
        self.xp = 0
        self.xp_to_level = 50
        self.type = None
        self.team = []
        self.original_position = None
        self.original_rotation = 0
        self.main = main
        if not main:
            self.position = None
        self.player = True
        self.base_health = self.health
        self.in_combat = False
        self.abilities.append(ability.Ability("Heavy Strike", self.base_damage, 1.5, 1, False))
        
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def square(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius
        a = self.position + forward * self.radius + right
        b = self.position - forward * self.radius + right
        c = self.position - forward * self.radius - right 
        d = self.position + forward * self.radius - right
        return [a, b, c, d]
    
    def draw(self, screen):
        if not self.dead and self.position:
            if not self.type:
                self.set_attributes(game_attributes["player_type"])
            match self.type:
                case "Triangle":
                    pygame.draw.polygon(
                    screen,
                    "white",
                    self.triangle(),
                    width
                )
                case "Square":
                    pygame.draw.polygon(
                    screen,
                    "white",
                    self.square(),
                    width
                )
                case _:
                    pygame.draw.circle(
                    screen,
                    "white",
                    (self.position.x, self.position.y),
                    self.radius,
                    width)
            
            if self.in_combat:
                self.draw_combat_attributes()
                draw_queue()

    def set_attributes(self, type):
        self.type = type
        match type:
            case "Triangle":
                self.health = 80
                self.base_health = 80
                self.initiative = 15
                self.damage = 8
            case "Square":
                self.health = 150
                self.base_health = 150
                self.initiative = 5
                self.damage = 15
            case _:
                pass
        self.team.append(self)
        print

    def post_encounter(self, xp_gained):
        self.xp += xp_gained
        self.dead = False
        if self.xp >= self.xp_to_level:
            self.level_up()
        self.health = self.base_health
        self.in_combat = False
        if self.main:
            self.position = self.original_position
            self.rotation = self.original_rotation
            self.encounter_chance = 0
            game_attributes["player"] = self
        else:
            self.position = None

    def level_up(self):
        xp = self.xp - self.xp_to_level
        self.level +=1
        self.xp = xp
        self.xp_to_level += math.ceil(self.level*0.8*20)
        match self.type:
            case "Triangle":
                self.base_health += 10
                self.initiative += 3
                self.damage += 1
            case "Square":
                self.base_health += 30
                self.initiative += 1
                self.damage += 3
            case _:
                self.base_health += 20
                self.initiative += 2
                self.damage += 2
        

    def rotate(self, dt):
        self.rotation += turn_speed * dt
    
    def update(self, dt):
        #print(f"Test update {self.team} and type: {self.type}")
        if not self.in_combat:
            keys = pygame.key.get_pressed()

            if self.encounter_chance < 100:
                if keys[pygame.K_a]:
                    self.rotate(-dt)
                if keys[pygame.K_d]:
                    self.rotate(dt)
                if keys[pygame.K_w]:
                    self.move(dt)
                    self.encounter_chance+=random.randint(1,3)
                if keys[pygame.K_s]:
                    self.move(-dt)
                    self.encounter_chance+=random.randint(1,3)
            
            if self.encounter_chance >= 100:
                enemies_count = random.randint(1,3)
                enemies = []
                hero_level = 0
                self.original_position = self.position
                self.in_combat = True
                
                for j in range(len(self.team)):
                    hero_level += self.team[j].level
                    pos = pygame.Vector2(game_attributes["width"]*((1+j)/(len(self.team)+1)), game_attributes["height"]*(62/100))
                    new_rotation = 180
                    if self.team[j].main :
                        self.position = pos
                        self.original_rotation = self.rotation
                        self.rotation = new_rotation
                    self.team[j].rotation = new_rotation
                    self.team[j].position = pos
                    self.team[j].original_position = self.original_position

                hero_level /= len(self.team)

                for i in range(enemies_count):
                    enemy = Enemy(game_attributes["width"]*((1+i)/(enemies_count+1)), 
                                        game_attributes["height"]*(1/5), 
                                        p_radius, 
                                        game_attributes["multiplier"],
                                        hero_level,
                                        self.team)
                    enemies.append(enemy)
                    
                #combat_attributes["players"] = self.team
                #combat_attributes["enemies"] = enemies
                encounter(self.team, enemies)

    def update_abilities(self):
        for ability in self.abilities:
            ability.update_damage(self.base_damage)   

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * dt * speed