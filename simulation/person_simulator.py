
from asyncio import current_task
from collections import deque
from datetime import time, timedelta
from os import name
import random
import datetime

from domain_model import room
from simulation.schedule_item import Schedule_Item
from simulation.pathfinding import Pathfinding

class Person_Simulator:

    MODE_UNDECIDED = 0
    MODE_OBLIGATION = 1
    MODE_LEISURE = 2

    def __init__(self, simulator, person, verbose = False):
        self.simulator = simulator
        self.verbose = verbose
        self.person = person
        self.schedule = []
        self.current_activity = None
        self.current_activity_location = None # kept outside of activity because activity has a list of options and may be shared among multiple people
        self.__reset_state_variables()

    def tick(self, current_time):
        """
            This function should be called every minute to update the persons position and activities
        """
        now = current_time.time()
        if current_time.hour == 0 and current_time.minute == 0:
            self.__reset_state_variables()
            self.__make_day_schedule(current_time)

        while len(self.schedule) > 0 and now > self.schedule[0].end_time:
            del self.schedule[0]

        if self.moving:
            self.__move_tick()
            return
        
        if self.mode == Person_Simulator.MODE_OBLIGATION:
            if now > self.current_task.end_time:
                self.__reset_state_variables()

        if self.mode == Person_Simulator.MODE_LEISURE:
            if self.current_activity_end is not None and now > self.current_activity_end:
                self.__reset_state_variables()
   
        if self.mode == Person_Simulator.MODE_UNDECIDED or self.mode == Person_Simulator.MODE_LEISURE:
            if now >= self.schedule[0].start_time:
                self.__reset_state_variables()
                self.mode = Person_Simulator.MODE_OBLIGATION
                self.current_task = self.schedule[0]
                self.__start_move(self.schedule[0].get_room())

                if(self.verbose):
                    room_description = "outside"
                    if(self.schedule[0].get_room() != None):
                        room_description = "in " + self.schedule[0].get_room().name
                    print(self.person.name, "started obligation", self.current_task.description, room_description)

        if self.mode == Person_Simulator.MODE_UNDECIDED:
            self.mode = Person_Simulator.MODE_LEISURE
            self.__pick_leisure_activity(current_time)
            return
        
    def __reset_state_variables(self):
        """
            Reset all variables associated to the current state (activity, path, task.)
        """
        self.current_task = None
        if self.current_activity is not None:
            self.current_activity.end_activity(self.current_activity_location)
            self.current_activity = None
            self.current_activity_location = None
        self.current_activity_end = None
        self.moving = False
        self.mode = Person_Simulator.MODE_UNDECIDED
        self.path = None


    def __pick_leisure_activity(self, current_time):
        """
            Picks and starts a leisure activity and duration for the current point in time.
        """
        ACTIVITY_INDEX = 0
        PRIORITY_INDEX = 1

        available_options = [option for option in self.person.leisure_activities if option[ACTIVITY_INDEX].is_available(current_time)]
        available_activities = [option[ACTIVITY_INDEX] for option in available_options]
        available_locations = [activity.get_location() for  activity in available_activities]
        weights = [self.__get_adjusted_weight(available_options[index][PRIORITY_INDEX], available_locations[index]) for index in range(len(available_activities))]

        current_activity_index = random.choices(population=range(len(weights)), weights=weights)[0]
        if current_activity_index is None:
            # fallback in case there are no valid activities just stand around and do nothing.
            return

        self.current_activity = available_activities[current_activity_index]
        self.current_activity_location = available_locations[current_activity_index]
        duration = self.current_activity.calculate_duration()
        if duration > 0:
            self.current_activity_end = (current_time + timedelta(minutes= duration)).time()
            if self.current_activity_end < current_time.time():
                self.current_activity_end = None

        self.current_activity.start_activity(self.current_activity_location)
        self.__start_move(self.current_activity_location)

        if(self.verbose):
            room_description = "outside"
            if(self.current_activity_location != None):
                room_description = "in " + self.current_activity_location.name
            print(self.person.name, "picked Leisure Activity", self.current_activity.name, room_description)

        

    def __get_adjusted_weight(self, weight, location):
        """
            Calculates the adjusted weight of a location based on current circumstances.
        """
        if location is None or location.is_outside:
            weight *= self.simulator.weather.get_quality()
        return weight

    def __move_tick(self):
        """
            Moves the person towards the room.
            this makes a step towards the next room in self.path.
        """
        if len(self.path) == 0:
            self.moving = False
            return
        
        next_room = self.path.popleft()
        self.person.move_to_room(next_room)


    def __start_move(self, target_room):
        """
            Starts moving the person towards the room.
            This calculates a path and sets the simulator to MODE_MOVEMENT
        """

        is_leaving_house = False

        # if target is outside of house, move to exit instead.
        if(target_room is None):
            target_room = self.simulator.house.get_exit()
            is_leaving_house = True

        # if person is inside of house, let them return home first.
        if(self.person.room is None):
            self.person.move_to_room(self.simulator.house.get_exit())

        # if either room still is None (e.g., because house has not implemented an exit) just move in / out without pathing.
        if target_room is None or self.person.room is None:
            self.moving = False
            self.person.move_to_room(target_room)
            return


        self.moving = True
        pathfinding = Pathfinding.instance()
        self.path = deque(pathfinding.get_path(self.simulator.house, self.person.room, target_room))

        # if leaving house, add one more transition from exit to gone.
        if(is_leaving_house):
            self.path.append(None)


        
    def __make_day_schedule(self, current_time):
        """
            Calculates the schedule for the day.
            This includes all obligations and sleep times.
        """
        self.schedule.clear()

        first_obligation_start = datetime.time(23,59) 
        last_obligation_end = datetime.time(0,0)

        for obligation in self.person.obligations:
            if obligation.happens_today(current_time):
                self.schedule.append(Schedule_Item(description = "Obligation: " + obligation.name,
                                           start_time=obligation.start_time,
                                           end_time=obligation.end_time, 
                                           activity_type=Schedule_Item.ACTIVITY_TYPE_OBLIGATION, 
                                           rooms = [obligation.location]))
                
                first_obligation_start = min(first_obligation_start,obligation.start_time)
                last_obligation_end = max(last_obligation_end, obligation.end_time)
        
        wakeup_time = min(first_obligation_start, self.person.wake_up_time)
        sleep_time = max(last_obligation_end, self.person.sleep_time)

        self.schedule.append(Schedule_Item(description = "Sleep(Morning)",
                                           start_time = time(0,00),
                                           end_time = wakeup_time, 
                                           activity_type = Schedule_Item.ACTIVITY_TYPE_SLEEP, 
                                           rooms = [self.person.sleep_room]))
        
        self.schedule.append(Schedule_Item(description = "Sleep(Evening)",
                                            start_time = sleep_time,
                                           end_time = time(23,59), 
                                           activity_type = Schedule_Item.ACTIVITY_TYPE_SLEEP, 
                                           rooms = [self.person.sleep_room]))
        
        self.schedule = sorted(self.schedule,key = lambda schedule_item: schedule_item.start_time)

