
import random
import pygame
from copy import copy, deepcopy
from datetime import timedelta
from collections import deque
from timeit import default_timer as timer

from view.main_window import Main_window

class Simulation:

    def __init__(self, display_user_interface = True, max_simulated_minutes = -1, prediction_delay_in_min = 0, random_seed = None):
        self.delta_time = timedelta(minutes= 1)
        self.display_user_interface = display_user_interface
        self.max_simulated_minutes = max_simulated_minutes;

        self.random_seed = random_seed
        self.running = False
        self.paused = False

        self.current_time = None
        self.predictions = deque()
        self.prediction_times = deque()

        self.prediction_system = None
        self.adaptation_controller = None
        self.data_recorder = None

        self.simulator = None

        self.window = None

        self.tick_count = 0
        self.prediction_delay_in_min = prediction_delay_in_min
    
    def get_current_prediction(self):
        if self.tick_count < self.prediction_delay_in_min:
            return None
        if len(self.predictions) == 0:
            return None
        return self.predictions[0]

    def get_current_prediction_time(self):
        if self.tick_count < self.prediction_delay_in_min:
            return None
        if len(self.prediction_times) == 0:
            return None
        return self.prediction_times[0]
    
    def pause(self):
        self.paused = True
    
    def resume(self):
        self.paused = False
    
    def is_paused(self):
        return self.paused

    def set_simulator(self, simulator):
        self.simulator = simulator

    def set_prediction_system(self,prediction_system):
        self.prediction_system = prediction_system
        self.prediction_system.set_simulation(self)

    def set_adaptation_controller(self, adaptation_controller):
        self.adaptation_controller = adaptation_controller
        self.adaptation_controller.set_simulation(self)

    def set_data_recorder(self,data_recorder):
        self.data_recorder = data_recorder
        self.data_recorder.set_simulation(self)

    def start(self):
        if self.simulator is None:
            raise Exception("Trying to simulate without a valid simulator. Did you forget to set a simulator?")
        
        random.seed(self.random_seed)

        # initialize simulator
        self.simulator.start_simulation()
        self.rooms = self.simulator.get_rooms()
        self.current_time = self.simulator.get_start_time()
        self.predicted_time = copy(self.current_time) + timedelta(minutes=self.prediction_delay_in_min)

        # show window if needed.
        if self.display_user_interface:
            self.window = Main_window(self)

        # start prediction, recoding and adaptation hooks
        if self.prediction_system is not None:
            self.prediction_system.on_simulation_start()

        if self.adaptation_controller is not None:
            self.adaptation_controller.on_simulation_start()
        
        if self.data_recorder is not None:
            self.data_recorder.on_simulation_start()

        # run simulation
        self.tick_count = 0
        self.running = True
        while self.running:
            if not self.paused:
                self.simulator.tick(self.current_time)

                # update prediction forecast
                if self.prediction_system is not None:
                    start_time = timer()
                    self.prediction_system.on_new_datapoint(copy(self.current_time),self.get_sensor_values())
                    prediction = self.prediction_system.predict_presence(self.predicted_time)
                    prediction_time = timer() - start_time
                    self.predictions.append(prediction)
                    self.prediction_times.append(prediction_time)
                
                # forward information to adaptation controller
                adaptation_time = -1
                if self.adaptation_controller is not None:
                    prediction = self.get_current_prediction()
                    if(prediction is not None):
                        prediction_time = self.get_current_prediction_time()
                        data_point = self.get_sensor_values()
                        start_time = timer()
                        self.adaptation_controller.on_new_prediction(copy(self.current_time), data_point, prediction, prediction_time )
                        adaptation_time = timer() - start_time

                # update data recorder
                if self.data_recorder is not None:
                    data_point = self.get_sensor_values()
                    prediction = self.get_current_prediction()
                    prediction_time = self.get_current_prediction_time()
                    self.data_recorder.on_new_datapoint(copy(self.current_time),data_point, prediction, self.simulator.get_weather_value(), prediction_time, adaptation_time)

                # update list of predictions
                if(len(self.predictions) > self.prediction_delay_in_min + 1):
                        self.predictions.popleft()
                        self.prediction_times.popleft()

                self.current_time = self.current_time + self.delta_time
                self.predicted_time = self.predicted_time + self.delta_time

            # update GUI
            if(self.display_user_interface):
                self.window.update_content()
                self.window.handle_events()
                self.window.frame_pause()
                if self.window.end_selected:
                    self.end()
                self.window = None

            # end condition
            self.tick_count += 1
            if self.max_simulated_minutes > 0 and self.tick_count >= self.max_simulated_minutes:
                self.end()

    def end(self):
        if(self.prediction_system != None):
            self.prediction_system.on_simulation_end()

        if self.data_recorder != None:
            self.data_recorder.on_simulation_end()

        if(self.display_user_interface):
                pygame.quit()

        self.running = False

    def get_sensor_values(self):
        sensor_values = []
        for room in self.rooms:
            sensor_values.append(bool(room.persons))
        return sensor_values

    def notify_visualization_refresh_needed(self):
            if self.window is not None:
                self.window.refresh_house_background()
