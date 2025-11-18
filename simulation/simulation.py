
import random
import pygame
import sys
from copy import copy, deepcopy
from datetime import timedelta
import time
from collections import deque
from timeit import default_timer as timer

from simulation.weather import Weather_Simulation
from view.main_window import Main_window
from simulation.person_simulator import Person_Simulator

class Simulation:
    
    def __init__(self, display_user_interface = True, max_simulated_minutes = -1, prediction_delay_in_min = 0, random_seed = None):
        self.delta_time = timedelta(minutes= 1)
        self.display_user_interface = display_user_interface
        self.max_simulated_minutes = max_simulated_minutes;

        self.random_seed = random_seed
        self.running = False

        self.house = None
        self.weather = None
        self.persons = []
        self.current_time = None
        self.predictions = deque()
        self.prediction_times = deque()
        self.adaptation_times = deque()
        self.person_simulators = []
        self.changes = []

        self.scenario = None
        self.prediction_system = None
        self.adaptation_controller = None
        self.data_recorder = None
        
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
    
    def get_current_adaptation_time(self):
        if self.tick_count < self.prediction_delay_in_min:
            return None
        if len(self.adaptation_times) == 0:
            return None
        return self.adaptation_times[0]


    def set_scenario(self,scenario):
        self.scenario = scenario # copy scenario in case it is expected to be reused.

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
        if(self.scenario == None):
            raise Exception("Trying to simulate without a valid scenario. Did you forget to set a simulation scenario?")
        
        random.seed(self.random_seed)

        # initialize from scenario (use deepcopy to avoid in-place modification)
        scenario_copy = deepcopy(self.scenario)
        self.house = scenario_copy.house
        self.weather = Weather_Simulation()
        self.rooms = []
        self.rooms.extend(self.house.rooms.values())
        self.rooms = sorted(self.rooms, key = lambda room: room.name)
        self.persons = scenario_copy.persons
        self.current_time = copy(scenario_copy.startTime)
        self.predicted_time = copy(self.current_time) + timedelta(minutes=self.prediction_delay_in_min)
        self.person_simulators = [Person_Simulator(self,person) for person in self.persons]
        self.changes = sorted(scenario_copy.changes, key = lambda change: change.datetime)


        # show window if needed.
        if self.display_user_interface:
            window = Main_window(scenario_copy)

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
            self.tick()

            # update prediction forecast
            if self.prediction_system is not None:
                start_time = timer()
                prediction = self.prediction_system.predict_presence(self.predicted_time)
                prediction_time = timer() - start_time
                self.predictions.append(prediction)
                self.prediction_times.append(prediction_time)
            
            # forward information to adaptation controller
            if self.adaptation_controller is not None:
                prediction = self.get_current_prediction()
                if(prediction is not None):
                    prediction_time = self.get_current_prediction_time()
                    data_point = self.get_sensor_values()
                    start_time = timer()
                    self.adaptation_controller.on_new_prediction(copy(self.current_time), data_point, prediction, prediction_time )
                    adaptation_time = timer() - start_time
                    self.adaptation_times.append(adaptation_time)

            # update data recorder
            if self.data_recorder is not None:
                data_point = self.get_sensor_values()
                prediction = self.get_current_prediction()
                prediction_time = self.get_current_prediction_time()
                adaptation_time = self.get_current_adaptation_time()
                self.data_recorder.on_new_datapoint(copy(self.current_time),data_point, prediction, self.weather.get_quality(), prediction_time, adaptation_time)

            # update list of predictions
            if(len(self.predictions) > self.prediction_delay_in_min + 1):
                    self.predictions.popleft()
                    self.prediction_times.popleft()
                    self.adaptation_times.popleft()

            # update GUI
            if(self.display_user_interface):
                time.sleep(0.1)
                window.update_content(self)
                if window.end_selected:
                    self.end()

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


    def tick(self):
        old_day = self.current_time.day
        self.current_time = self.current_time + self.delta_time
        self.predicted_time = self.predicted_time + self.delta_time

        if(old_day != self.current_time.day):
            random.shuffle(self.person_simulators)

        self.weather.tick(self.current_time)

        while self.changes and self.current_time == self.changes[0].datetime:
            self.changes[0].execute(self)
            self.changes.pop(0)
            print("Change executed at ", self.current_time)

        for person_simulator in self.person_simulators:
            person_simulator.tick()
    

    def get_sensor_values(self):
        sensor_values = []
        for room in self.rooms:
            sensor_values.append(bool(room.persons))
        return sensor_values
    
    def remove_person(self, person):
        person.move_to_room(None)
        self.persons.remove(person)
        self.person_simulators = [sim for sim in self.person_simulators if sim.person != person]

    def add_person(self,person):
        self.persons.append(person)
        self.person_simulators.append(Person_Simulator(self,person))
