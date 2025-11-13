
from collections import deque
from datetime import time, timedelta
import random

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
        self.current_activity = None
        self.reset_state_variables()

    def reset_state_variables(self):
        """
            Reset all variables associated to the current state (activity, path, task.)
        """
        self.current_task = None
        if self.current_activity is not None:
            self.current_activity.end_activity()
            self.current_activity = None
        self.current_activity_end = None
        self.moving = False
        self.mode = Person_Simulator.MODE_UNDECIDED
        self.path = None


    def tick(self):
        now = self.simulation.current_time.time()
        if self.simulation.current_time.day != self.last_simulated_day:
            self.reset_state_variables()
            self.make_day_schedule()

        while len(self.schedule) > 0 and now > self.schedule[0].end_time:
            del self.schedule[0]

        if self.moving:
            self.move_tick()
            return
        
        if self.mode == Person_Simulator.MODE_OBLIGATION:
            if now > self.current_task.end_time:
                self.reset_state_variables()

        if self.mode == Person_Simulator.MODE_LEISURE:
            if self.current_activity_end is not None and now > self.current_activity_end:
                self.reset_state_variables()
   
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
        weights = [self.__get_adjusted_weight(option[1], option[0]) for option in available_options]

        self.current_activity = random.choices(population=available_activities, weights=weights)[0]
        if self.current_activity is None:
            # fallback in case there are no valid activities just stand around and do nothing.
            return
        
        duration = self.current_activity.calculate_duration()
        if duration > 0:
            self.current_activity_end = (self.simulation.current_time + timedelta(minutes= duration)).time()
            if self.current_activity_end < self.simulation.current_time.time():
                self.current_activity_end = None
        self.current_activity.start_activity()
        self.start_move(self.current_activity.location)

    def __get_adjusted_weight(self, weight, activity):
        """
            Calculates the adjusted weight of an activity based on current circumstances.
        """
        if activity.location is None or activity.location.is_outside:
            weight *= self.simulation.weather.get_quality()
        return weight

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

