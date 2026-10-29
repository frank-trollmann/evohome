
from copy import copy, deepcopy


from simulation.random_generator import Simulation_Random_Generator
from simulation.simulator_base import Simulator_Base
from simulation.weather import Weather_Simulation
from simulation.person_simulator import Person_Simulator


class Scenario_Simulator(Simulator_Base):
    """
        A simulator based on a Scenario.
        The simulator simulates the daily routine of all persons within the scenario. 
        Movement between activities is simulated based on the rooms and transitions in the house.
    """
    
    def __init__(self, scenario, simulation, verbose = False):
        """
            Constructor.

            Args:
                scenario (Scenario) The simulated scenario
                simulation (Simuation): Refernece to the simulation.
                verbose (bool): Whether the simulator should print debug information.
        """

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
        """
            Initializes the simulator at the start of the simulation.

        """
        scenario_copy = deepcopy(self.scenario)
        self.house = scenario_copy.house
        self.weather = Weather_Simulation()
        self.rooms = []
        self.rooms.extend(self.house.rooms.values())
        self.rooms = sorted(self.rooms, key = lambda room: room.name)
        self.persons = [] + scenario_copy.persons
        self.person_simulators = [Person_Simulator(self,person, verbose=self.verbose) for person in self.persons]
        self.changes = sorted(scenario_copy.changes, key = lambda change: change.datetime)
        self.current_gradual_changes = []

    def get_room_by_name(self, name):
        """
            retrieves the room by name.

            Args:
                name (string) the name of the room

            Returns:
                Room: the room
        """
        return self.house.rooms[name]

    def get_rooms(self):
        """
            Retrieves all rooms.

            Returns:
                list<Room>: all rooms
        """
        return self.rooms
    
    def get_transitions(self):
        """
            Retrieves all transitions.

            Returns:
                dictionary: A dictionary representation of transitions with source name (string) as key and target room (Room) as value
        """
        return self.house.transitions
    
    def get_start_time(self):
        """
            Retrieves the start time of the scenario.

            Returns:
                datetime: the starting time and date
        """
        return copy(self.scenario.startTime)
    
    def tick(self, current_time):
        """
            One tick in the simulation. 
            Simulates one minute in the scenario and sets presence of persons in rooms accordingly. 

            Args:
                current_time (datetime) the current time.

        """
        if(current_time.hour == 0 and current_time.minute == 0):
            self.on_new_day()

        self.weather.tick(current_time)

        while self.changes and current_time == self.changes[0].datetime:
            print(f"Change {type(self.changes[0])} executed at", current_time)
            self.changes[0].execute(self)
            self.changes.pop(0)
            

        for person_simulator in self.person_simulators:
            person_simulator.tick(current_time)

    def on_new_day(self):
        """
            Callback method to be called on new day start.
        """
        Simulation_Random_Generator._generator.shuffle(self.person_simulators)
        changes = self.current_gradual_changes[:] # copy list to avoid concurrent modification. (on_next_day is deleting finished gradual changes)
        for gradual_change in  changes:
            gradual_change.on_next_day(self)

    def get_weather_value(self):
        """
            retrieves the weather value

            Returns:
                float: the suitability of the current weather for outside activities.
        """
        return self.weather.get_quality()
    
    def get_background_image(self):
        """
            Retrieves the background image of the scenario.

            Returns: 
                string: the url of the background image
        """
        return self.scenario.background_image

    def remove_person(self, person):
        """
            Remove a person from the simulation. 

            Args:
                person (Person): the person to remove

        """
        person.move_to_room(None)
        self.persons.remove(person)
        self.person_simulators = [sim for sim in self.person_simulators if sim.person != person]

    def add_person(self,person):
        """
            Adds a person to the simulation. 

            Args:
                person (Person): the person to add

        """
        self.persons.append(person)
        self.person_simulators.append(Person_Simulator(self,person))

    def add_gradual_change(self,change):
        """
            Adds a gradual change to the simulation.

            Args:
                change (Gradual_Change): the change to add
                
        """
        self.current_gradual_changes.append(change)

    def remove_gradual_change(self,change):
        """
            Removes a gradual change from the simulation.

            Args:
                change (Gradual_Change): the change to remove
                
        """
        self.current_gradual_changes.remove(change)

    def notify_visualization_refresh_needed(self):
        """
            This function can be used in the simulation to notify that an update to the visualization is needed.
            Can, for example, be used to let the visualization know that the background image / room needs to be redrawn.
        """
        if self.simulation is not None:
            self.simulation.notify_visualization_refresh_needed()