
from collections import deque
from datetime import time
from operator import truediv
import random

from domain_model.room import Room
from simulation import simulation
from simulation.schedule_item import Schedule_Item
from simulation.pathfinding import Pathfinding

class Person_Simulator:

    MODE_ACTIVITY = 0
    MODE_MOVEMENT = 1

    def __init__(self, simulation, person):
        self.simulation = simulation
        self.person = person
        self.schedule = []
        self.last_simulated_day = -1
        self.current_schedule_item = None
        self.mode = Person_Simulator.MODE_ACTIVITY
        self.path = None

    def tick(self):
        if self.simulation.current_time.day != self.last_simulated_day:
            self.make_day_schedule()

        now = self.simulation.current_time.time()

        while len(self.schedule) > 0 and now > self.schedule[0].end_time:
            del self.schedule[0]

        if self.mode == Person_Simulator.MODE_MOVEMENT:
            self.move()
        elif self.mode == Person_Simulator.MODE_ACTIVITY:

            # go to schedule position, if not there
            if now > self.schedule[0].start_time:
                if(self.current_schedule_item != self.schedule[0]):
                    self.current_schedule_item = self.schedule[0]
                    self.start_movement(self.schedule[0].get_room())
                    #self.person.move_to_room(self.schedule[0].get_room())
                return

            # pick leisure activity if not picked already
            if(self.current_schedule_item != None):
                self.current_schedule_item = None
                leisure_rooms = [self.person.sleep_room, None]
                leisure_rooms.extend(self.simulation.house.get_rooms_by_function(Room.FUNCTION_LEISURE))
                picked_room = random.choice(leisure_rooms)
                self.start_movement(picked_room)
                #self.person.move_to_room(picked_room)

    def move(self):
        """
            Moves the person towards the room.
            this makes a step towards the next room in self.path.
        """
        if len(self.path) == 0:
            self.mode = Person_Simulator.MODE_ACTIVITY
            return
        
        next_room = self.path.popleft()
        self.person.move_to_room(next_room)


    def start_movement(self, target_room):
        """
            Starts moving the person towards the room.
            This calculates a path and sets the simulator to MODE_MOVEMENT
        """
        if target_room is None or self.person.room is None:
            self.person.move_to_room(target_room)
            self.mode = Person_Simulator.MODE_ACTIVITY
            return
        
        pathfinding = Pathfinding.instance()
        self.path = deque(pathfinding.get_path(self.simulation.house, self.person.room, target_room))
        self.mode = Person_Simulator.MODE_MOVEMENT

        



    def make_day_schedule(self):
        self.schedule.clear()
        self.last_simulated_day = self.simulation.current_time.day

        self.schedule.append(Schedule_Item(description = "Sleep(Morning)",
                                           start_time=time(0,00),
                                           end_time=self.person.wake_up_time, 
                                           activity_type=Schedule_Item.ACTIVITY_TYPE_SLEEP, 
                                           rooms = [self.person.sleep_room]))
        for obligation in self.person.obligations:
            if obligation.happens_today(self.simulation.current_time):
                self.schedule.append(Schedule_Item(description = "Obligation: " + obligation.name,
                                           start_time=obligation.start_time,
                                           end_time=obligation.end_time, 
                                           activity_type=Schedule_Item.ACTIVITY_TYPE_OBLIGATION, 
                                           rooms = [obligation.location]))
        self.schedule.append(Schedule_Item(description = "Sleep(Evening)",
                                            start_time=self.person.sleep_time,
                                           end_time= time(23,59), 
                                           activity_type=Schedule_Item.ACTIVITY_TYPE_SLEEP, 
                                           rooms = [self.person.sleep_room]))
        
        self.schedule = sorted(self.schedule,key = lambda schedule_item: schedule_item.start_time)

