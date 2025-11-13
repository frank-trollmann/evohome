
from collections import deque
from datetime import time
from operator import truediv
import random

from domain_model.room import Room
from simulation import simulation
from simulation.schedule_item import Schedule_Item
from simulation.pathfinding import Pathfinding

class Person_Simulator:

    MODE_UNDECIDED = 0
    MODE_OBLIGATION = 1
    MODE_LEISURE = 2

    def __init__(self, simulation, person):
        self.simulation = simulation
        self.person = person
        self.schedule = []
        self.last_simulated_day = -1
        self.current_task = None
        self.moving = False
        self.mode = Person_Simulator.MODE_LEISURE
        self.path = None


    def tick(self):
        now = self.simulation.current_time.time()
        if self.simulation.current_time.day != self.last_simulated_day:
            self.make_day_schedule()

        while len(self.schedule) > 0 and now > self.schedule[0].end_time:
            del self.schedule[0]

        if self.moving:
            self.move_tick()
            return
        
        if self.mode == Person_Simulator.MODE_OBLIGATION:
            if now > self.current_task.end_time:
                self.current_task = None
                self.mode = Person_Simulator.MODE_UNDECIDED
   
        if self.mode == Person_Simulator.MODE_UNDECIDED or self.mode == Person_Simulator.MODE_LEISURE:
            if now >= self.schedule[0].start_time:
                self.mode = Person_Simulator.MODE_OBLIGATION
                self.current_task = self.schedule[0]
                self.start_move(self.schedule[0].get_room())

        if self.mode == Person_Simulator.MODE_UNDECIDED:
            self.mode = Person_Simulator.MODE_LEISURE
            self.pick_leisure_activity()
            return
        


    def pick_leisure_activity(self):
        available_options = [option for option in self.person.leisure_activities if option[0].is_available(self.simulation.current_time)]
        available_activities = [option[0] for option in available_options]
        weights = [option[1] for option in available_options]

        choice = random.choices(population=available_activities, weights=weights)[0]
        self.start_move(choice.location)

    def move_tick(self):
        """
            Moves the person towards the room.
            this makes a step towards the next room in self.path.
        """
        if len(self.path) == 0:
            self.moving = False
            return
        
        next_room = self.path.popleft()
        self.person.move_to_room(next_room)


    def start_move(self, target_room):
        """
            Starts moving the person towards the room.
            This calculates a path and sets the simulator to MODE_MOVEMENT
        """
        if target_room is None or self.person.room is None:
            self.moving = False
            self.person.move_to_room(target_room)
            return
        
        self.moving = True
        pathfinding = Pathfinding.instance()
        self.path = deque(pathfinding.get_path(self.simulation.house, self.person.room, target_room))

        



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

