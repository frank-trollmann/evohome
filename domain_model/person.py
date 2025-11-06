
from domain_model.obligation import Obligation


class Person:
    """
        This class represents a person living in the house.
    """
    def __init__(self, name, ui_color, wake_up_time, sleep_time):
        """
            Constructor.
            Args:
                name (string): the name of the person.
                ui_color (string): the color used to represent this person in the user interface.
                wake_up_time (time): the time the person naturally wakes up.
                sleep_time (time): the time the person naturally goes to sleep.
        """
        self.name = name
        self.room = None
        self.ui_color = ui_color

        self.wake_up_time = wake_up_time
        self.sleep_time = sleep_time
        self.sleep_room = None
        
        self.obligations = []

    
    def move_to_room(self,new_room):
        """
            Moves the person to a new room.
            Deregisters the person from the previous room.

            Args:
                new_room (Room): the room to move to.
        """
        if self.room != None:
            self.room.persons.remove(self)
        self.room = new_room
        if new_room != None:
            new_room.persons.append(self)

    def add_obligation(self,name, start_time, end_time, location = None, weekdays = None):
        """
            Adds an obligation to the person.
            
            Args:
                name (string): the name of the obligation.
                start_time (time): the start time of the obligation.
                end_time (time): the end time of the obligation.
                location (Room): the location where the obligation happens. None means the location happens outside of the house.
                weekdays (int[]): the weekdays where the obligation happens. 0 = Monday, 6 = Sunday. None means every day.
        """
        self.obligations.append(Obligation(name,start_time,end_time,location,weekdays))