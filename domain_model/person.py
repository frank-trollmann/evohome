
from domain_model.obligation import Obligation


class Person:
    def __init__(self, name, ui_color, wake_up_time, sleep_time):
        self.name = name
        self.room = None
        self.ui_color = ui_color

        self.wake_up_time = wake_up_time
        self.sleep_time = sleep_time
        self.sleep_room = None
        
        self.obligations = []



    
    def move_to_room(self,new_room):
        if self.room != None:
            self.room.persons.remove(self)
        self.room = new_room
        if new_room != None:
            new_room.persons.append(self)

    def add_obligation(self,name, start_time, end_time, location = None, weekdays = None):
        self.obligations.append(Obligation(name,start_time,end_time,location,weekdays))