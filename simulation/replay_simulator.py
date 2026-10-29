
from math import e
from domain_model.person import Person
from simulation.simulator_base import Simulator_Base

from datetime import datetime
import pandas as pd;


class Replay_Simulator(Simulator_Base):
    """
        A simulator based on a replay of a recording.
        The recording is provided as a Pandas Dataframe with the following requirements:
        - The dataset is a timeseries indexed over datetime with one entry per minute
        - Minutes that do not exist are filled in with the last known value
        - Each room should have a boolean column with the room's name
    """


    def __init__(self, rooms, data, start_date = None, transitions = {}, background_image = None):
        """
            Constructor.

            Args:
                rooms (list<string>) the list of rooms
                data (DataFrame): A pandas dataframe with the simulation data.
                transitions (dictionary): An optional dictionary representation of graph edges with source name (string) as key and target room (Room) as value
                background_image (string): Url of the background image
        """
        self.rooms = rooms
        self.rooms_by_name = {room.name: room for room in rooms}
        self.transitions = transitions
        
        min_time = data.index.min()
        if start_date is None:
            self.start_date = min_time
        else:
            # enforce using timezone from dataframe to ensure compatibility of keys.
            self.start_date = datetime(year = start_date.year, 
                                                month = start_date.month, 
                                                day = start_date.day,
                                                hour=start_date.hour, 
                                                minute = start_date.minute, 
                                                tzinfo = min_time.tz)
            
        self.data = data
        self.background_image = background_image
        self.last_data = None

        self.DummyPerson = Person(name = "Dummy", ui_color=(0, 100, 0))

    def get_room_by_name(self, name):
        """
            retrieves the room by name.

            Args:
                name (string) the name of the room

            Returns:
                Room: the room
        """
        return self.rooms_by_name[name]
    
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
        return self.transitions
    
    def get_start_time(self):
        """
            Retrieves the start time of the scenario.

            Returns:
                datetime: the starting time and date
        """
        return self.start_date
    
    def get_background_image(self):
        """
            Retrieves the background image of the scenario.

            Returns: 
                string: the url of the background image
        """
        return self.background_image
    
    def tick(self, current_time):
        """
            One tick in the simulation. 
            Sets persons into each room, depending on whether the room is occupied in the dataset.

            Args:
                current_time (datetime) the current time.

        """
        if(self.data.index.__contains__(current_time)):
            self.last_data = self.data.loc[pd.Timestamp(current_time)]
        for room in self.rooms:
            if(self.last_data is not None and self.last_data[room.name]):
                room.persons = [self.DummyPerson]
            else:
                room.persons = []

