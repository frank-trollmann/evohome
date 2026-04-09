
from math import e
from domain_model.person import Person
from simulation.simulator_base import Simulator_Base

from datetime import datetime
import pandas as pd;


class Replay_Simulator(Simulator_Base):
    """
        A simulator based on a replay of a recording.
        The recording is provided as a pandas dataframe with the following requirements:
        - The dataset is a timeseries indexed over datetime with one entry per minute
        - Minutes that are not exist are filled in with the last known value
        - each room should have a boolean column in the dataset
    """


    def __init__(self, rooms, data, start_date = None, transitions = {}, background_image = None):
        """
            Constructor.
            
            :param rooms: A list of rooms
            :param data: A pandas dataframe indexed over time with a column for each room.
            :param data: A pandas dataframe indexed over time with a column for each room.
            :param transitions: A dictionary representation of graph edges with source name (string) as key and target room (Room) as value
            :param background_image: Url of the background image
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
        return self.rooms_by_name[name]
    
    def get_rooms(self):
        return self.rooms
    
    def get_transitions(self):
        return self.transitions
    
    def get_start_time(self):
        return self.start_date
    
    def get_background_image(self):
        return self.background_image
    
    def tick(self, current_time):
        if(self.data.index.__contains__(current_time)):
            self.last_data = self.data.loc[pd.Timestamp(current_time)]
        for room in self.rooms:
            if(self.last_data is not None and self.last_data[room.name]):
                room.persons = [self.DummyPerson]
            else:
                room.persons = []

