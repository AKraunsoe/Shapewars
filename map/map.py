import pygame
import random

from globalvariables.constants import MAP_WIDTH, MAP_HEIGHT, CORRIDOR_WIDTH, MIN_HALL_LENGTH, MAX_HALL_LENGTH, WHITE
from globalvariables.gameattributes import game_attributes

class Map():
    def __init__(self, level, screen):
        self.edges= self.create_edges()
        self.level= level
        self.screen= screen
        self.outer_collision_box= pygame.Rect(-MAP_WIDTH, -MAP_HEIGHT, MAP_WIDTH, MAP_HEIGHT)
        self.corridors= self.create_corridors() 

    def create_edges(self):
        edges = []
        #top
        edges.append(pygame.Rect(-(MAP_WIDTH/2), -(MAP_HEIGHT/2), MAP_WIDTH, 1))
        #bottom
        edges.append(pygame.Rect(-(MAP_WIDTH/2), (MAP_HEIGHT/2), MAP_WIDTH, 1))
        #left
        edges.append(pygame.Rect(-(MAP_WIDTH/2), -(MAP_HEIGHT/2), 1, MAP_HEIGHT))
        #right
        edges.append(pygame.Rect((MAP_WIDTH/2), -(MAP_HEIGHT/2), 1, MAP_HEIGHT))
        return edges

    def create_corridors(self):
        corridors = []
        rotation = False if random.randint(1, 2) == 1 else True
        x_divisible = 4 if not rotation else 2
        y_divisble = 4 if rotation else 2
        add_width_x = CORRIDOR_WIDTH if rotation else 0
        add_width_y = CORRIDOR_WIDTH if not rotation else 0
        bot_right_y = game_attributes["height"]/y_divisble + add_width_y
        top_left_y = game_attributes["height"]/y_divisble - add_width_y
        bot_right_x = game_attributes["width"]/x_divisible + add_width_x
        top_left_x = game_attributes["width"]/x_divisible - add_width_x

        line_length = random.randint(MIN_HALL_LENGTH, MAX_HALL_LENGTH)
        
        bot_right_rect = None
        top_left_rect = None

        if not rotation:
            bot_right_rect = pygame.Rect(bot_right_x, bot_right_y, line_length, 1)
            top_left_rect = pygame.Rect(top_left_x, top_left_y, line_length, 1)
        else:
            bot_right_rect = pygame.Rect(bot_right_x, bot_right_y, 1, line_length)
            top_left_rect = pygame.Rect(top_left_x, top_left_y, 1, line_length)

        endpoints = {}
        if rotation:
            endpoints["bot_right"] = [(bot_right_x, bot_right_y, bot_right_x, bot_right_y+line_length), (bot_right_x, bot_right_y+line_length, bot_right_x, bot_right_y)]
            endpoints["top_left"] = [(top_left_x, top_left_y, top_left_x, top_left_y+line_length), (top_left_x, top_left_y+line_length, top_left_x, top_left_y)]
        else:
            endpoints["bot_right"] = [(bot_right_x, bot_right_y, bot_right_x+line_length, bot_right_y), (bot_right_x+line_length, bot_right_y, bot_right_x, bot_right_y)]
            endpoints["top_left"] = [(top_left_x, top_left_y, top_left_x+line_length, top_left_y), (top_left_x+line_length, top_left_y, top_left_x, top_left_y)]

        corridors.append((bot_right_rect, top_left_rect))
        #return corridors
        #rotation = "down" if rotation else "right"

        while len(endpoints)>0:
            #previous_rotation = rotation

            bot_right = endpoints["bot_right"]
            bot_right_length = len(bot_right)
            new_bot_right_endpoints = []
            new_top_left_endpoints = []
            for i in range(bot_right_length):
                rotation = False if random.randint(1, 2) == 1 else True
                line_length = random.randint(MIN_HALL_LENGTH, MAX_HALL_LENGTH)
                start_coords = (bot_right[0], bot_right[1])
                end_coords = (bot_right[2], bot_right[3])
                if rotation:
                    # previous line is vertical, new line is vertical
                    if start_coords[0] == end_coords[0]:
                        bot_right_rect_from_start = None
                        trimmed_length_bot_right_start = self.collides_with(start_coords, line_length, "up", corridors)
                        if isinstance(trimmed_length_bot_right_start, int):
                            bot_right_rect_from_start = pygame.Rect(coords[0], coords[1], trimmed_length_bot_right_start, 1)

                            new_bot_right_endpoints.append(((coords[0], coords[1]),(coords[0]+trimmed_length_bot_right_start, coords[1])))
                        else:
                            bot_right_rect_from_start = trimmed_length_bot_right_start
                        
                        trimmed_length_top_left_start = self.collides_with(start_coords, line_length, "up", corridors)
                        top_left_rect_from_start = pygame.Rect(coords[0], coords[1]-CORRIDOR_WIDTH, trimmed_length_top_left_start, 1)

                        corridors.append(bot_right_rect_from_start, top_left_rect_from_start)
                        
                    # previous line is horizontal, new line is vertical    
                    elif start_coords[1] == end_coords[1]:
                        pass
                else:
                    if True:
                        
                        pass
                    else:
                        pass
            

            top_left = endpoints["top_left"]
            top_left_length = len(top_left)
            
            for j in range(top_left_length):
                line_length = random.randint(MIN_HALL_LENGTH, MAX_HALL_LENGTH)
                coords = top_left[0]
                if rotation:
                    pass
                else:
                    pass

            if len(new_bot_right_endpoints) == 0:
                del endpoints["bot_right"]
            else:
                endpoints["bot_right"] = new_bot_right_endpoints
            
            if len(new_top_left_endpoints) == 0:
                del endpoints["top_left"]
            else:
                endpoints["bot_right"] = new_bot_right_endpoints

            #previous_rotation = rotation
            """
            if previous_rotation == "down":
                if rotation:
                    previous_rotation = "right"
                else:
                    previous_rotation = "down"
            else:
                if rotation:
                    previous_rotation = "down"
                else:
                    previous_rotation = "right"
            """
            
            break

        #top = pygame.draw.aaline(screen, WHITE, top_start, top_end, 1)
        #bottom = pygame.draw.aaline(screen, WHITE, bottom_start, bottom_end, 1)

        
        return corridors


    def collides_with(self, start_coords, length, direction, corridors):
        result = length
        all_sides = corridors + self.edges
        for corridor in all_sides:
            for side in corridor:
                match direction:
                    case "up":
                        end_y = start_coords[1]-result
                        if start_coords[0] > side.left and start_coords[0] < side.right and end_y < side.top:
                            result = result-(side.top-end_y)
                    case "left":
                        end_x = start_coords[0]-result
                        if start_coords[1] > side.bottom and start_coords[1] < side.top and end_x > side.left:
                            result = result-(side.left-end_x)
                    case "down":
                        end_y = start_coords[1]+result
                        if start_coords[0] > side.left and start_coords[0] < side.right and end_y < side.top:
                            result = result-(end_y-side.top)
                    case "right":
                        end_x = start_coords[0]+result
                        if start_coords[1] > side.bottom and start_coords[1] < side.top and end_x > side.left:
                            result = result-(end_x-side.left)

        return result

            