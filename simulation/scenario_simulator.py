
import random
from copy import copy, deepcopy


from simulation.simulator_base import Simulator_Base
from simulation.weather import Weather_Simulation
from simulation.person_simulator import Person_Simulator


class Scenario_Simulator(Simulator_Base):
    def __init__(self, scenario, simulation, verbose = False):
        self.scenario = scenario
        self.simulation = simulation
        self.verbose = verbose
        
        self.house = None
        self.rooms = None
        self.weather = None
        self.persons = []
        self.person_simulators = []
        self.changes = []
        self.current_gradual_changes = []
    
    def start_simulation(self):
        scenario_copy = deepcopy(self.scenario)
        self.house = scenario_copy.house
        self.weather = Weather_Simulation()
        self.rooms = []
        self.rooms.extend(self.house.rooms.values())
        self.rooms = sorted(self.rooms, key = lambda room: room.name)
        self.persons = scenario_copy.persons
        self.person_simulators = [Person_Simulator(self,person, verbose=self.verbose) for person in self.persons]
        self.changes = sorted(scenario_copy.changes, key = lambda change: change.datetime)
        self.current_gradual_changes = []

    def get_room_by_name(self, name):
        return self.house.rooms[name]

    def get_rooms(self):
        return self.rooms
    
    def get_transitions(self):
        return self.house.transitions
    
    def get_start_time(self):
        return copy(self.scenario.startTime)
    
    def tick(self, current_time):
        if(current_time.hour == 0 and current_time.minute == 0):
            self.on_new_day()

        self.weather.tick(current_time)

        while self.changes and current_time == self.changes[0].datetime:
            self.changes[0].execute(self)
            self.changes.pop(0)
            print("Change executed at ", current_time)

        for person_simulator in self.person_simulators:
            person_simulator.tick(current_time)

    def on_new_day(self):
        random.shuffle(self.person_simulators)
        changes = self.current_gradual_changes[:] # copy list to avoid concurrent modification. (on_next_day is deleting finished gradual changes)
        for gradual_change in  changes:
            gradual_change.on_next_day(self)

    def get_weather_value(self):
        return self.weather.get_quality()
    
    def get_background_image(self):
        return self.scenario.background_image

    def remove_person(self, person):
        person.move_to_room(None)
        self.persons.remove(person)
        self.person_simulators = [sim for sim in self.person_simulators if sim.person != person]

    def add_person(self,person):
        self.persons.append(person)
        self.person_simulators.append(Person_Simulator(self,person))

    def add_gradual_change(self,change):
        self.current_gradual_changes.append(change)

    def remove_gradual_change(self,change):
        self.current_gradual_changes.remove(change)

    def notify_visualization_refresh_needed(self):
        if self.simulation is not None:
            self.simulation.notify_visualization_refresh_needed()