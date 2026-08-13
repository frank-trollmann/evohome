from tkinter import EXCEPTION
import pygame
from pygame.locals import *
from pygame import Surface
from pygame._sdl2 import Window

import time
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"
pygame.init()

class Main_window:
   
    def __init__(self, simulation):
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 20)

        self.simulation = simulation

        self.sleep_time = 0.1
        self.paused = False

        self.house_background = self.__create_house_background()
        self.draw_surface = Surface(self.house_background.get_size())
        self.screen = pygame.display.set_mode((500,500), flags=DOUBLEBUF | RESIZABLE)
        self.end_selected = False

        Window.from_display_module().maximize()

    def update_content(self):
        """
            Updates the visualization with the current content of the simulation
        """
        self.draw_surface.blit(self.house_background,(0,0),None)
        self.__draw_persons(self.draw_surface, self.simulation)
        self.__draw_predictions(self.draw_surface,self.simulation)
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
        self.__draw_controls(self.screen)
        self.__draw_time(self.screen,self.simulation)
        pygame.display.flip()


    def frame_pause(self):
        """
            Pauses the application appropriately to the speed set in the window.
            Can be used to speed up / slow down visualization
        """
        time.sleep(self.sleep_time)

    
    def handle_events(self):
        """
            handles input related events.
        """
        events = pygame.event.get(eventtype=[pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]) 

        for event in events:
            if event.type == pygame.QUIT:
                self.end_selected = True
            
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE:
                    self.__toggle_pause()
                elif event.key == pygame.K_LEFT:
                    self.__slow_down()
                elif event.key == pygame.K_RIGHT:
                    self.__speed_up()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                screen_width = self.screen.get_size()[0]
                if(self.__event_over_button(event, self.__get_pause_button_position(screen_width))):
                    self.__toggle_pause()
                if(self.__event_over_button(event, self.__get_slower_button_position(screen_width))):
                    self.__slow_down()
                if(self.__event_over_button(event, self.__get_faster_button_position(screen_width))):
                    self.__speed_up()
        pygame.event.clear()
                    
    def __create_house_background(self):
        """
            Create the static background image of the house. The image consists of ...
                - The floor plan image (if one is provided)
                - Nodes for all rooms
                - Edges for room transitions
            The returned object is a pygame surface with dimensions equal to the background image.
            If no background image is provided, the dimenions are calculated so they can accomodate the coordinates of all rooms.
        """
        # initialize canvas based on background image or room coordinates
        simulator = self.simulation.simulator
        rooms = simulator.get_rooms()
        transitions = simulator.get_transitions()

        background_image = simulator.get_background_image()
        if background_image != None:
            house_image = pygame.image.load(background_image)
            house_background = pygame.Surface([house_image.get_width(),house_image.get_height()])
            house_background.blit(house_image,(0,0),None)
            pygame.display.set_mode((house_image.get_width(),house_image.get_height()), flags=DOUBLEBUF | RESIZABLE)
        else:
            max_x = max(rooms, key = lambda room: room.x).x
            max_y = max(rooms, key = lambda room: room.y).y
            house_background = pygame.Surface([max_x + 20,max_y + 20])
            house_background.fill((255,255,255))

        # draw rooms
        for room in rooms:
            pygame.draw.circle(surface = house_background,
                               center = (room.x,room.y),
                               radius = 10,
                               color = (0,0,255))
        
        # draw room connections
        for start_room_key in transitions.keys():
            for end_room in transitions[start_room_key]:
                start_room = simulator.get_room_by_name(start_room_key)
                pygame.draw.line(surface = house_background,
                                start_pos = (start_room.x,start_room.y),
                                end_pos = (end_room.x, end_room.y),
                                width = 5,
                                color = (0,0,255))
        return house_background

    
    def __draw_persons(self, surface, simulation):
        """
            draw all persons onto the surface
        """
        rooms = self.simulation.simulator.get_rooms()

        for room in rooms:
            current_person_index = 0
            for person in room.persons:
                x_offset = 20 * current_person_index 
                y_offset = 20
                pygame.draw.circle(surface = surface,
                               center = (room.x + x_offset,room.y + y_offset),
                               radius = 8,
                               color = person.ui_color)
                current_person_index += 1

    def __draw_predictions(self, surface, simulation):
        """
            draw information about the predictions
        """
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
        

    def __draw_time(self, surface, simulation):
        """
            draw the current time to the surface
        """
        text = simulation.current_time.strftime("%m/%d/%Y, %H:%M:%S, %A")
        text_surface = self.font.render(text,True,(0,0,0),(255,255,255))
        surface.blit(text_surface, (10,10))
    
    def __draw_controls(self,surface):
        """
            draws window controls to the given surface
        """
        screen_width = surface.get_size()[0]

        slower_pos = self.__get_slower_button_position(screen_width)
        self.__draw_button(surface, "<<", slower_pos)

        play_pause_pos = self.__get_pause_button_position(screen_width)
        if self.simulation.is_paused():
            play_pause_text =  ">"
        else:
            play_pause_text =  "||"
        self.__draw_button(surface, play_pause_text, play_pause_pos)

        faster_pos = self.__get_faster_button_position(screen_width)
        self.__draw_button(surface, ">>", faster_pos)

    def __speed_up(self):
        self.sleep_time = max(self.sleep_time/ 2.0, 0.0000001)

    def __slow_down(self):
        self.sleep_time = min(self.sleep_time*2, 2.0)

    def __toggle_pause(self):
        if self.simulation.is_paused():
            self.simulation.resume()
        else:
            self.simulation.pause()

    def __draw_button(self, surface, text,  position):
        """
            draw a single button to the given surface
        """
        size = self.__get_button_size()
        pygame.draw.rect(surface,(200,200,200), position + self.__get_button_size())
        slower_text_surface = self.font.render(text,True,(0,0,0),(200,200,200))

        offset_x = (size[0] - slower_text_surface.get_size()[0])/2
        offset_y = (size[1] - slower_text_surface.get_size()[1])/2

        surface.blit(slower_text_surface,(position[0] + offset_x, position[1] + offset_y))
    
    def __event_over_button(self, event, button_position):
        click_pos = event.pos
        button_size = self.__get_button_size()
        hit_x = click_pos[0] > button_position[0] and click_pos[0] < button_position[0] + button_size[0]
        hit_y = click_pos[1] > button_position[1] and click_pos[1] < button_position[1] + button_size[1]
        return hit_x and hit_y

    def __get_slower_button_position(self, width):
        return (width-150,10)
    
    def __get_faster_button_position(self, width):
        return (width-50,10)
    
    def __get_pause_button_position(self,width):
        return (width-100,10)
    
    def __get_button_size(self):
        return (40,30)
    


