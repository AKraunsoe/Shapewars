import sys
import random
import math

sys.path.append('../circleshape') 

from circleshape import CircleShape
from constants import LINE_WIDTH as width
from constants import PLAYER_TURN_SPEED as turn_speed
from constants import PLAYER_SPEED as speed
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

    def rotate(self, dt):
        self.rotation += turn_speed * dt
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * dt * speed

class Enemy(Unit):
    def __init__(self, x, y, radius, multiplier, hero_level):
        super().__init__(x, y, radius)
        self.setAttributes(multiplier, hero_level)

    def setAttributes(self, multiplier, hero_level):
        self.level = math.ceil(hero_level*0.5*multiplier)
        self.initiative = random.randint(10+self.level, (10+self.level)*multiplier)
        self.health = self.health + ((self.level-1)*(20*multiplier))
        self.base_damage = self.base_damage + ((self.level-1)*(1*multiplier))