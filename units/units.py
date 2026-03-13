
import random
import math

from circleshape import CircleShape
import encounter as encounter
from globalvariables.constants import LINE_WIDTH as width
from globalvariables.constants import PLAYER_TURN_SPEED as turn_speed
from globalvariables.constants import PLAYER_SPEED as speed
from globalvariables.constants import PLAYER_RADIUS as p_radius
import pygame

class Unit(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.initiative = 10
        self.health = 100
        self.ability_points = 0
        self.base_damage = 10
        self.abilities = []
        self.level = 1

class Player(Unit):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = 0
        self.encounter_chance = 0
        self.xp = 0
        self.xp_to_level = 100
        self.type = "Circle"
        self.team = [self]
        
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
    
    def draw(self, screen, type):
        match type:
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
        self.type = type

    def rotate(self, dt):
        self.rotation += turn_speed * dt
    
    def update(self, dt, game_attributes):
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
        
        if self.encounter_chance == 100:
            enemies_count = random.randint(1,3)
            enemies = []
            hero_level = 0
            
            for j in range(len(self.team)):
                hero_level += self.team[j].level

            hero_level /= len(self.team)

            print(f"current pos: {self.position}")

            for i in range(enemies_count):
                enemies.append(Enemy(self.position[0]-100+(i*100), 
                                     self.position[1]+100, 
                                     p_radius, 
                                     game_attributes["multiplier"],
                                     hero_level))
            encounter.Encounter(self.team, enemies)
        

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * dt * speed

class Enemy(Unit):
    def __init__(self, x, y, radius, multiplier, hero_level):
        super().__init__(x, y, radius)
        self.set_attributes(multiplier, hero_level)
        self.xp_provided = (20 * self.level) * (self.level/hero_level)

    def set_attributes(self, multiplier, hero_level):
        self.level = math.ceil(hero_level*0.5*multiplier)
        self.initiative = random.randint(10+self.level, (10+self.level)*multiplier)
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
        pygame.draw.polygon(
        screen,
        "white",
        self.star(),
        width
        )
            