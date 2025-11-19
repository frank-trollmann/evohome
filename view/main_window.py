import pygame
from pygame.locals import *
from pygame import Surface
from pygame._sdl2 import Window

import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"
pygame.init()

class Main_window:
   
    def __init__(self, scenario):
        pygame.font.init()

        self.house_background = self.create_house_background(scenario)
        self.draw_surface = Surface(self.house_background.get_size())
        self.screen = pygame.display.set_mode((500,500), flags=DOUBLEBUF | RESIZABLE)
        self.end_selected = False

        Window.from_display_module().maximize()
    
    """
        Create the static background image of the house. The image consists of ...
            - The floor plan image (if one is provided)
            - Nodes for all rooms
            - Edges for room transitions
        The returned object is a pygame surface with dimensions equal to the background image.
        If no background image is provided, the dimenions are calculated so they can accomodate the coordinates of all rooms.
    """
    def create_house_background(self, scenario):

        # initialize canvas based on background image or room coordinates
        if scenario.background_image != None:
            house_image = pygame.image.load(scenario.background_image)
            house_background = pygame.Surface([house_image.get_width(),house_image.get_height()])
            house_background.blit(house_image,(0,0),None)
            pygame.display.set_mode((house_image.get_width(),house_image.get_height()), flags=DOUBLEBUF | RESIZABLE)
        else:
            max_x = max(scenario.house.rooms.values(), key = lambda room: room.x).x
            max_y = max(scenario.house.rooms.values(), key = lambda room: room.y).y
            house_background = pygame.Surface([max_x + 20,max_y + 20])
            house_background.fill((255,255,255))

        # draw rooms
        house = scenario.house
        for room in house.rooms.values():
            pygame.draw.circle(surface = house_background,
                               center = (room.x,room.y),
                               radius = 10,
                               color = (0,0,255))
        
        # draw room connections
        for start_room_key in house.transitions.keys():
            for end_room in house.transitions[start_room_key]:
                start_room = house.rooms[start_room_key]
                pygame.draw.line(surface = house_background,
                                start_pos = (start_room.x,start_room.y),
                                end_pos = (end_room.x, end_room.y),
                                width = 5,
                                color = (0,0,255))

        return house_background

    """
        draw all persons onto the screen.
    """
    def draw_persons(self, surface, simulation):
        
        for room in simulation.house.rooms.values():
            current_person_index = 0
            for person in room.persons:
                x_offset = 20 * current_person_index
                y_offset = 20
                pygame.draw.circle(surface = surface,
                               center = (room.x + x_offset,room.y + y_offset),
                               radius = 8,
                               color = person.ui_color)
                current_person_index += 1

    def draw_predictions(self,surface, simulation):
        current_prediction = simulation.get_current_prediction()
        if(current_prediction is None):
            return
        
        index = 0
        for room in simulation.rooms:
            if(current_prediction[index]):
                pygame.draw.circle(surface = surface,
                                center = (room.x,room.y-20),
                                radius = 10,
                                color = (255,255,0))
            index += 1
        

    def draw_time(self,surface,simulation):
        text = simulation.current_time.strftime("%m/%d/%Y, %H:%M:%S, %A")
        text_surface = pygame.font.SysFont('Comic Sans MS', 20).render(text,True,(0,0,0),(255,255,255))
        surface.blit(text_surface, (10,10))


    def update_content(self, simulation):
        self.draw_surface.blit(self.house_background,(0,0),None)
        self.draw_persons(self.draw_surface, simulation)
        self.draw_predictions(self.draw_surface,simulation)
        self.draw_time(self.draw_surface,simulation)

        screen_size = self.screen.get_size()
        draw_size = self.draw_surface.get_size()
        scale_factor_x = screen_size[0] / draw_size[0]
        scale_factor_y = screen_size[1] / draw_size[1]
        scale_factor = min(scale_factor_x, scale_factor_y)
        scaled_draw_surface = pygame.transform.scale_by(self.draw_surface, scale_factor)
        scaled_size = scaled_draw_surface.get_size()
        offset_x = (screen_size[0] - scaled_size[0]) / 2.0
        offset_y = (screen_size[1] - scaled_size[1]) / 2.0


        self.screen.fill((255,255,255))
        self.screen.blit(scaled_draw_surface,(offset_x,offset_y))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end_selected = True