
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
        self.scroll_pos = self.position
        self.collision_box = None
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
                    self.collision_box = pygame.draw.polygon(
                    screen,
                    "white",
                    self.triangle(),
                    width
                )
                case "Square":
                    self.collision_box = pygame.draw.polygon(
                    screen,
                    "white",
                    self.square(),
                    width
                )
                case _:
                    self.collision_box = pygame.draw.circle(
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
                self.health = 100
                pass
        self.team.append(self)

    def post_encounter(self, xp_gained):
        self.xp += xp_gained
        self.dead = False
        if self.xp >= self.xp_to_level:
            self.level_up()
        self.health = self.base_health
        self.in_combat = False
        self.ability_points = 0
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
        self.check_collision(self.scroll_pos)
    
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
                    #self.encounter_chance+=(1/random.randint(3,5))
                if keys[pygame.K_s]:
                    self.move(-dt)
                    #self.encounter_chance+=(1/random.randint(3,5))
            
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
                    
                encounter(self.team, enemies)

    def update_abilities(self):
        for ability in self.abilities:
            ability.update_damage(self.base_damage)   

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        new_pos = self.scroll_pos + (forward * dt * speed)
        self.check_collision(new_pos)
        

    def check_collision(self, new_pos):
        dx = math.ceil(self.scroll_pos.x-new_pos.x)
        dy = math.ceil(self.scroll_pos.y-new_pos.y)
        edges = game_attributes["current_map"].edges
        corridors = game_attributes["current_map"].corridors
        #print(f"edges: {edges}\ncorridors: {corridors}")
        iterations = 0
        while True:
            iterations +=1
            new_corridors=[]
            new_edges=[]
            recalculate = False
            for i in range(len(edges)):
                new_edge = edges[i].move(dx, dy)
                # top, left
                match i:
                    case 0:
                        check_dy_top = abs(new_edge.y+new_edge.height) < abs(self.position.y + self.radius) + abs(dy)
                        if new_edge.colliderect(self.collision_box) and (check_dy_top):
                            recalculate = True
                            #print(f"current_top_edge: {edges[i]}")
                            #print(f"new_edge: {new_edge}\nmy_position: {self.position}")
                            if check_dy_top:
                                pre_dy = dy
                                #print(f"dy pre update: {pre_dy}")
                                dy = self.position.y - new_edge.y-self.radius
                                #print(f"updated top dy: {self.position.y - new_edge.y+self.radius}")
                                if pre_dy == dy:
                                    recalculate = False
                            #print(f"overlap edge dx: {dx}")
                            #print(f"overlap edge dy: {dy}")
                            if recalculate:
                                break
                    case 1:
                        check_dy_bot = abs(new_edge.y) > abs(self.position.y - self.radius) - abs(dy)
                        if new_edge.colliderect(self.collision_box) and (check_dy_bot):
                            recalculate = True
                            #print(f"current_bot_edge: {edges[i]}")
                            #print(f"new_edge: {new_edge}\nmy_position: {self.position}")
                            if check_dy_bot:
                                pre_dy = dy
                                #print(f"dy pre update: {pre_dy}")
                                dy = self.position.y - new_edge.y+self.radius
                                #print(f"updated top_left dy: {self.position.y - new_edge.y-self.radius}")
                                if pre_dy == dy:
                                    recalculate = False
                            
                            #print(f"overlap edge dx: {dx}")
                            #print(f"overlap edge dy: {dy}")
                            if recalculate:
                                break
                    case 2:
                        check_dx_left = abs(new_edge.x+new_edge.width) < abs(self.position.x + self.radius) + abs(dx)
                        if new_edge.colliderect(self.collision_box) and (check_dx_left):
                            recalculate = True
                            #print(f"current_left_edge: {edges[i]}")
                            #print(f"new_edge: {new_edge}\nmy_position: {self.position}")
                            if check_dx_left:
                                pre_dx = dx
                                #print(f"dx pre update: {pre_dx}")
                                dx = self.position.x - new_edge.x-self.radius
                                #print(f"update bot dx: {self.position.x - new_edge.x+self.radius}")
                                if dx == pre_dx:
                                    recalculate = False
                            #print(f"overlap edge dx: {dx}")
                            #print(f"overlap edge dy: {dy}")
                            if recalculate:
                                break
                    case 3:
                        check_dx_right = abs(new_edge.x) > abs(self.position.x - self.radius) - abs(dx)
                        if new_edge.colliderect(self.collision_box) and (check_dx_right):
                            recalculate = True
                            #print(f"curren_right_edge: {edges[i]}")
                            #print(f"new_edge: {new_edge}\nmy_position: {self.position}")
                            if check_dx_right:
                                pre_dx = dx
                                #print(f"dx pre update: {pre_dx}")
                                dx = self.position.x - new_edge.x+self.radius
                                #print(f"update top_left  dx: {self.position.x - new_edge.x-self.radius}")
                                if dx == pre_dx:
                                    recalculate = False     
                            #print(f"overlap edge dx: {dx}")
                            #print(f"overlap edge dy: {dy}")
                            if recalculate:
                                break                    
                
                new_edges.append(new_edge)

            if not recalculate:
                for corridor in corridors:
                    new_bot_right = corridor[0].move(dx, dy)
                    new_top_left = corridor[1].move(dx, dy)
                    check_dx_bot_right = abs(new_bot_right.x+new_bot_right.width) < abs(self.position.x + self.radius) + abs(dx) if new_bot_right.width == 1 else False
                    check_dy_bot_right = abs(new_bot_right.y+new_bot_right.height) < abs(self.position.y + self.radius) + abs(dy) if new_bot_right.height == 1 else False
                    if new_bot_right.colliderect(self.collision_box) and (check_dx_bot_right or check_dy_bot_right):
                        recalculate = True
                        #print(f"current_bot_right_corridor: {corridor[0]}")
                        #print(f"new_corridor: {new_bot_right}\nmy_position: {self.position}")
                        if check_dx_bot_right:
                            pre_dx = dx
                            #print(f"dx pre update: {pre_dx}")
                            dx = self.position.x - new_bot_right.x+self.radius
                            #print(f"update top dx: {self.position.x - new_bot_right.x+self.radius}")
                            if dx == pre_dx:
                                recalculate = False
                        if check_dy_bot_right:
                            pre_dy = dy
                            #print(f"dy pre update: {pre_dy}")
                            dy = self.position.y - new_bot_right.y+self.radius
                            #print(f"updated top dy: {self.position.y - new_bot_right.y+self.radius}")
                            if pre_dy == dy:
                                recalculate = False
                        #print(f"overlap corridor dx: {dx}")
                        #print(f"overlap corridor dy: {dy}")
                        if recalculate:
                            break

                    check_dx_top_left = abs(new_top_left.x) > abs(self.position.x - self.radius) - abs(dx) if new_bot_right.width == 1 else False
                    check_dy_top_left = abs(new_top_left.y) > abs(self.position.y - self.radius) - abs(dy) if new_bot_right.height == 1 else False
                    if new_top_left.colliderect(self.collision_box) and (check_dx_top_left or check_dy_top_left):
                        recalculate = True
                        #print(f"curren_bottom_corridor: {corridor[1]}")
                        #print(f"new_corridor: {new_top_left}\nmy_position: {self.position}")
                        if check_dx_top_left:
                            pre_dx = dx
                            #print(f"dx pre update: {pre_dx}")
                            dx = self.position.x - new_top_left.x-self.radius
                            #print(f"update bottom dx: {self.position.x - new_top_left.x-self.radius}")
                            if dx == pre_dx:
                                recalculate = False
                        if check_dy_top_left:
                            pre_dy = dy
                            #print(f"dy pre update: {pre_dy}")
                            dy = self.position.y - new_top_left.y-self.radius
                            #print(f"updated bottom dy: {self.position.y - new_top_left.y-self.radius}")
                            if pre_dy == dy:
                                recalculate = False
                        #print(f"overlap corridor dx: {dx}")
                        #print(f"overlap corridor dy: {dy}")
                        if recalculate:
                            break

                    new_corridors.append((new_bot_right, new_top_left))

            if not recalculate or iterations==3:
                break

        game_attributes["current_map"].corridors = new_corridors
        game_attributes["current_map"].edges = new_edges

        #print(f"new_edges: {new_edges}\nnew_corridors: {new_corridors}")
        self.scroll_pos = new_pos