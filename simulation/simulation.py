
import pygame
import sys
from copy import copy, deepcopy
from datetime import timedelta
import time
from collections import deque

from view.main_window import Main_window
from simulation.person_simulator import Person_Simulator

class Simulation:
    
    def __init__(self, display_user_interface = True, max_simulated_minutes = -1, prediction_delay_in_min = 0):
        self.delta_time = timedelta(minutes= 1)
        self.display_user_interface = display_user_interface
        self.max_simulated_minutes = max_simulated_minutes;

        self.house = None
        self.persons = []
        self.current_time = None
        self.predicted_time = None
        self.predictions = deque()
        self.person_simulators = []
        self.changes = []

        self.scenario = None
        self.prediction_system = None
        self.data_recorder = None
        
        self.tick_count = 0
        self.prediction_delay_in_min = prediction_delay_in_min
    
    def get_current_prediction(self):
        if self.tick_count < self.prediction_delay_in_min:
            return None
        if len(self.predictions) == 0:
            return None
        return self.predictions[0]

    def set_scenario(self,scenario):
        self.scenario = scenario # copy scenario in case it is expected to be reused.

    def set_prediction_system(self,prediction_system):
        self.prediction_system = prediction_system
        self.prediction_system.set_simulation(self)

    def set_data_recorder(self,data_recorder):
        self.data_recorder = data_recorder
        self.data_recorder.set_simulation(self)

    def start(self):
        if(self.scenario == None):
            raise Exception("Trying to simulate without a valid scenario. Did you forget to set a simulation scenario?")
        
        # initialize from scenario (use deepcopy to avoid in-place modification)
        scenario_copy = deepcopy(self.scenario)
        self.house = scenario_copy.house
        self.rooms = []
        self.rooms.extend(self.house.rooms.values())
        self.rooms = sorted(self.rooms, key = lambda room: room.name)
        self.persons = scenario_copy.persons
        self.current_time = copy(scenario_copy.startTime)
        self.predicted_time = copy(self.current_time) + timedelta(minutes=self.prediction_delay_in_min)
        self.person_simulators = []
        for person in self.persons:
            self.person_simulators.append(Person_Simulator(self, person))
        self.changes = sorted(scenario_copy.changes, key = lambda change: change.datetime)


        # show window if needed.
        if self.display_user_interface:
            window = Main_window(scenario_copy)

        if self.prediction_system != None :
            self.prediction_system.on_simulation_start()
        
        if self.data_recorder != None:
            self.data_recorder.on_simulation_start()

        # run simulation
        self.tick_count = 0
        while True:
            self.tick()

            # update prediction forecast
            if self.prediction_system is not None:
                prediction = self.prediction_system.predict_presence(self.predicted_time)
                self.predictions.append(prediction)
            
            # update data recorder
            if self.data_recorder is not None:
                data_point = self.get_sensor_values()
                prediction = self.get_current_prediction()
                self.data_recorder.on_new_datapoint(copy(self.current_time),data_point, prediction)

            # update list of predictions
            if(len(self.predictions) > self.prediction_delay_in_min + 1):
                    self.predictions.popleft()

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

        sys.exit()


    def tick(self):
        self.current_time = self.current_time + self.delta_time
        self.predicted_time = self.predicted_time + self.delta_time

        if(self.changes and self.current_time == self.changes[0].datetime):
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
