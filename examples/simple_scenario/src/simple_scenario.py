from operator import is_
from domain_model.changes.leisure_activity_add import Leisure_Activity_Add_Change
from domain_model.changes.leisure_activity_remove_change import Leisure_Activity_Remove_Change
from domain_model.changes.move_in_change import Move_In_Change
from domain_model.changes.obligation_add_change import Obligation_Add_Change
from domain_model.changes.obligation_remove_change import Obligation_Remove_Change
from domain_model.leisure_activity import Leisure_Activity
from domain_model.obligation import Obligation
from domain_model.scenario import Scenario_Configuration
from domain_model.changes.move_out_change import Move_Out_Change
from domain_model.house import House
from domain_model.room import Room
from domain_model.person import Person

from datetime import datetime
from datetime import time


def create_simple_scenario():
    scenario = Scenario_Configuration()
    scenario.background_image = "examples/simple_scenario/images/house_1.png"

    house = House()
    scenario.house = house
    scenario.startTime = datetime(year = 2020, month = 6, day = 6, hour = 0, minute = 0)

    # create rooms and transitions
    hallway_1 = Room("Hallway 1", 230, 370)
    hallway_2 = Room("Hallway 2", 530, 370)
    bedroom1 = Room("Bedroom 1", 663, 490, functions = [Room.FUNCTION_SLEEP])
    bedroom2 = Room("Bedroom 2", 170, 230, functions = [Room.FUNCTION_SLEEP])
    bedroom3 = Room("Bedroom 3", 170, 500, functions = [Room.FUNCTION_SLEEP])
    office = Room("Storage", 100, 370, functions = [Room.FUNCTION_OFFICE, Room.FUNCTION_LEISURE], ressources=["PC"])
    bathroom_1 = Room("Bath 1", 670, 320, functions = [Room.FUNCTION_BATHROOM])
    bathroom_2 = Room("Bath 2", 260, 260, functions = [Room.FUNCTION_BATHROOM])
    kitchen = Room("Kitchen", 510, 180, functions = [Room.FUNCTION_COOK])
    living_room = Room("Living Room", 460, 500, functions = [Room.FUNCTION_LEISURE, Room.FUNCTION_EAT], ressources=["TV", "Couch"])
    porch = Room("Porch", 500, 740, functions = [Room.FUNCTION_LEISURE], is_outside=True)

    house.add_room(hallway_1)
    house.add_room(hallway_2)
    house.add_room(bedroom1)
    house.add_room(bedroom2)
    house.add_room(bedroom3)
    house.add_room(office)
    house.add_room(bathroom_1)
    house.add_room(bathroom_2)
    house.add_room(kitchen)
    house.add_room(living_room)
    house.add_room(porch)


    house.add_transtion(bedroom2, hallway_1)
    house.add_transtion(bedroom3, hallway_1)
    house.add_transtion(office, hallway_1)
    house.add_transtion(bathroom_2, hallway_1)
    house.add_transtion(hallway_1, hallway_2) 
    house.add_transtion(hallway_2, kitchen)
    house.add_transtion(hallway_2, living_room)
    house.add_transtion(living_room, porch)
    house.add_transtion(hallway_2, bedroom1)
    house.add_transtion(bedroom1, bathroom_1)


    # create Obligations
    work_parent_1_obligation = Obligation("Work", 
                                start_time= time(7,00), 
                                end_time = time(14,00), 
                                location = office, 
                                weekdays = [0,1,2,3,4])
    work_parent_2_obligation = Obligation("Work", 
                                start_time= time(6,00), 
                                end_time = time(16,00), 
                                location = None, 
                                weekdays = [0,1,2,3,4])
    get_kids_obligation = Obligation("Get kids", 
                                start_time= time(14,00), 
                                end_time = time(15,00), 
                                location = None, 
                                weekdays = [0,1,2,3,4])
    prepare_dinner_obligation = Obligation("Cook Dinner", 
                                start_time= time(16,00), 
                                end_time = time(17,00), 
                                location = kitchen)
    breakfast_obligation = Obligation("Breakfast", 
                                start_time= time(6,00), 
                                end_time = time(6,30), 
                                location = living_room,
                                weekdays = [0,1,2,3,4])
    prepare_lunch_obligation = Obligation("Prepare Lunch", 
                                start_time= time(11,00), 
                                end_time = time(12,00), 
                                location = living_room,
                                weekdays = [5,6])
    study_obligation = Obligation("Study", 
                                start_time= time(10,00), 
                                end_time = time(11,00), 
                                location = bedroom2,
                                weekdays = [5,6])
    lunch_obligation = Obligation("Lunch", 
                                start_time= time(12,00), 
                                end_time = time(13,00), 
                                location = living_room,
                                weekdays = [5,6])
    dinner_obligation = Obligation("Dinner", 
                                start_time= time(17,00), 
                                end_time = time(18,00), 
                                location = living_room)
    bring_to_bed_obligation = Obligation("Read Bedtime Story", 
                                start_time= time(19,30), 
                                end_time = time(20,00), 
                                location = bedroom2)
    school_obligation = Obligation("School", 
                                start_time= time(7,00), 
                                end_time = time(15,00), 
                                location = None, 
                                weekdays = [0,1,2,3,4])
    piano_practice = Obligation("Piano Practice", 
                                start_time= time(13,00), 
                                end_time = time(15,00), 
                                weekdays = [5,6])
    chess_club = Obligation("Chess Club", 
                                start_time= time(15,00), 
                                end_time = time(17,00), 
                                weekdays = [5,6])
    
    # create leisure_activities
    alone_time_parent_1 = Leisure_Activity("Alone Time", 
                                            location = bedroom1,
                                            min_duration= 30, 
                                            max_duration= 120)
    play_pc = Leisure_Activity("Play Games",
                                            location = office, 
                                            min_duration = 60, 
                                            max_duration=240,
                                            required_ressources=["PC"])
    watch_tv = Leisure_Activity("TV",
                                            location = living_room, 
                                            min_duration=10, 
                                            max_duration=60,
                                            required_ressources=["TV", "Couch"])

    alone_time_parent_2 = Leisure_Activity("Alone Time", 
                                            location = bedroom1, 
                                            min_duration=30, 
                                            max_duration=60)
    porch_reading = Leisure_Activity("Porch reading", 
                                            location = porch, 
                                            min_duration=30, 
                                            max_duration=240)
    inside_reading = Leisure_Activity("Inside reading", 
                                            location = living_room, 
                                            min_duration=30, 
                                            max_duration=240,
                                            required_ressources=["Couch"])

    alone_time_child_1 = Leisure_Activity("Alone Time", 
                                            bedroom2, 
                                            min_duration=20, 
                                            max_duration=120)
    shopping = Leisure_Activity("Shopping", 
                                            location = None, 
                                            weekdays = [0,1,2,3,4,5], 
                                            min_duration=60, 
                                            max_duration=240)

    alone_time_child_2 = Leisure_Activity("Alone Time", 
                                            location = bedroom3, 
                                            min_duration=30, 
                                            max_duration=120)


    
     # create persons
    parent_1 = Person("Arny", (255, 255, 0),wake_up_time= time(6,00), sleep_time = time(22,00))
    parent_1.sleep_room = bedroom1
    scenario.add_person(parent_1)
    parent_1.add_obligation(breakfast_obligation)
    parent_1.add_obligation(work_parent_1_obligation)
    parent_1.add_obligation(get_kids_obligation)
    parent_1.add_obligation(prepare_dinner_obligation)
    parent_1.add_obligation(dinner_obligation)
    parent_1.add_obligation(lunch_obligation)
    parent_1.add_obligation(study_obligation)
    parent_1.add_leisure_activity(alone_time_parent_1, 1)
    parent_1.add_leisure_activity(play_pc, 2)
    parent_1.add_leisure_activity(watch_tv, 2)

    parent_2 = Person("Betty", (0, 255, 255),wake_up_time = time(5,00), sleep_time = time(21,00))
    parent_2.sleep_room = bedroom1
    scenario.add_person(parent_2)
    parent_2.add_obligation(work_parent_2_obligation)
    parent_2.add_obligation(dinner_obligation)
    parent_2.add_obligation(bring_to_bed_obligation)
    parent_2.add_obligation(lunch_obligation)
    parent_2.add_obligation(prepare_lunch_obligation)
    parent_2.add_obligation(piano_practice)
    parent_2.add_leisure_activity(alone_time_parent_2,1)
    parent_2.add_leisure_activity(porch_reading,4)
    parent_2.add_leisure_activity(inside_reading,2)


    child_1 = Person("Coline", (255, 0, 255),wake_up_time = time(6,00), sleep_time = time(20,00))
    child_1.sleep_room = bedroom2
    scenario.add_person(child_1)
    child_1.add_obligation(breakfast_obligation)
    child_1.add_obligation(school_obligation)
    child_1.add_obligation(dinner_obligation)
    child_1.add_obligation(bring_to_bed_obligation)
    child_1.add_obligation(lunch_obligation)
    child_1.add_obligation(study_obligation)
    child_1.add_leisure_activity(alone_time_child_1,4)
    child_1.add_leisure_activity(shopping,2)
    child_1.add_leisure_activity(watch_tv,2)

    child_2 = Person("Dave", (255, 0, 0),wake_up_time = time(6,00), sleep_time = time(21,00))
    child_2.sleep_room = bedroom3
    scenario.add_person(child_2)
    child_2.add_obligation(breakfast_obligation)
    child_2.add_obligation(school_obligation)
    child_2.add_obligation(dinner_obligation)
    child_2.add_obligation(lunch_obligation)
    child_2.add_obligation(chess_club)
    child_2.add_leisure_activity(alone_time_child_2,2)
    child_2.add_leisure_activity(watch_tv,4)
    child_2.add_leisure_activity(play_pc,4)

    # create changes
    # child 2 leaves for three months
    child_2_move_out = Move_Out_Change(datetime(year = 2021, month = 6, day = 2, hour = 0, minute = 0), child_2)
    child_2_move_in = Move_In_Change(datetime(year = 2021, month = 9, day = 2, hour = 0, minute = 0), child_2)
    scenario.changes.append(child_2_move_out)
    scenario.changes.append(child_2_move_in)

    # parent 1 changes time for cooking
    remove_cooking_change = Obligation_Remove_Change(datetime(year = 2021, month = 3, day = 2, hour = 0, minute = 0), parent_1, "Cook")
    cook2_obligation = Obligation("Cook2", 
                                start_time= time(15,30), 
                                end_time = time(16,30), 
                                location = kitchen, 
                                weekdays = [0,1,2,3,4,5])
    add_cooking_change = Obligation_Add_Change(datetime(year = 2021, month = 3, day = 2, hour = 0, minute = 0), parent_1, cook2_obligation)
    scenario.changes.append(remove_cooking_change)
    scenario.changes.append(add_cooking_change) 

    # child 2 picks up cooking practice instead of playing video games 
    remove_play_change = Leisure_Activity_Remove_Change(datetime(year = 2022, month = 1, day = 2, hour = 0, minute = 0), child_2, "Play Games")
    practice_cooking = Leisure_Activity("Practice Cooking", 
                                            location = kitchen, 
                                            min_duration=30, 
                                            max_duration=60)
    add_practice_cooking_change = Leisure_Activity_Add_Change(datetime(year = 2022, month = 1, day = 2, hour = 0, minute = 0), child_2, practice_cooking, 4)
    scenario.changes.append(remove_play_change)
    scenario.changes.append(add_practice_cooking_change) 

    return scenario

