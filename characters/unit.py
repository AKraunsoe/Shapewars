from circleshape import CircleShape
from constants import LINE_WIDTH as width
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
        
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def square(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        d = self.position + forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen, type):
        match type:
            case "triangle":
                pygame.draw.polygon(
                screen,
                "white",
                self.triangle(),
                width
            )
            case "square":
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