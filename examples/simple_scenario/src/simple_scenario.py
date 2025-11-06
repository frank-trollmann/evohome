from domain_model.changes.move_in_change import Move_In_Change
from domain_model.changes.obligation_remove_change import Obligation_Remove_Change
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
    scenario.startTime = datetime(year = 2020, month = 6, day = 1, hour = 0, minute = 0)

    # create rooms and transitions
    hallway_1 = Room("Hallway 1", 230, 370)
    hallway_2 = Room("Hallway 2", 530, 370)
    bedroom1 = Room("Bedroom 1", 663, 490, [Room.FUNCTION_SLEEP])
    bedroom2 = Room("Bedroom 2", 170, 230, [Room.FUNCTION_SLEEP])
    bedroom3 = Room("Bedroom 3", 170, 500, [Room.FUNCTION_SLEEP])
    storage = Room("Storage", 100, 370, [Room.FUNCTION_OFFICE, Room.FUNCTION_LEISURE])
    bathroom_1 = Room("Bath 1", 670, 320, [Room.FUNCTION_BATHROOM])
    bathroom_2 = Room("Bath 2", 260, 260, [Room.FUNCTION_BATHROOM])
    kitchen = Room("Kitchen", 510, 180, [Room.FUNCTION_COOK])
    living_room = Room("Living Room", 460, 500, [Room.FUNCTION_LEISURE, Room.FUNCTION_EAT])
    porch = Room("Porch", 500, 740, [Room.FUNCTION_LEISURE])

    house.add_room(hallway_1)
    house.add_room(hallway_2)
    house.add_room(bedroom1)
    house.add_room(bedroom2)
    house.add_room(bedroom3)
    house.add_room(storage)
    house.add_room(bathroom_1)
    house.add_room(bathroom_2)
    house.add_room(kitchen)
    house.add_room(living_room)
    house.add_room(porch)


    house.add_transtion(bedroom2, hallway_1)
    house.add_transtion(bedroom3, hallway_1)
    house.add_transtion(storage, hallway_1)
    house.add_transtion(bathroom_2, hallway_1)
    house.add_transtion(hallway_1, hallway_2) 
    house.add_transtion(hallway_2, kitchen)
    house.add_transtion(hallway_2, living_room)
    house.add_transtion(living_room, porch)
    house.add_transtion(hallway_2, bedroom1)
    house.add_transtion(bedroom1, bathroom_1)

    # create persons
    parent1 = Person("Arny", (255, 255, 0),wake_up_time= time(6,00), sleep_time = time(22,00))
    parent1.sleep_room = bedroom1
    parent1.move_to_room(bedroom1)
    scenario.persons.append(parent1)

    parent2 = Person("Betty", (0, 255, 255),wake_up_time = time(5,00), sleep_time = time(21,00))
    parent2.sleep_room = bedroom1
    parent2.move_to_room(bedroom1)
    scenario.persons.append(parent2)

    child1 = Person("Coline", (255, 0, 255),wake_up_time = time(6,00), sleep_time = time(20,00))
    child1.sleep_room = bedroom2
    child1.move_to_room(bedroom2)
    scenario.persons.append(child1)

    child2 = Person("Dave", (255, 0, 0),wake_up_time = time(6,00), sleep_time = time(21,00))
    child2.sleep_room = bedroom3
    child2.move_to_room(bedroom3)
    scenario.persons.append(child2)

    # add Obligations
    work_parent_1_obligation = Obligation("Work", 
                                start_time= time(7,00), 
                                end_time = time(14,00), 
                                location = storage, 
                                weekdays = [0,1,2,3,4,5])
    work_parent_2_obligation = Obligation("Work", 
                                start_time= time(6,00), 
                                end_time = time(16,00), 
                                location = None, 
                                weekdays = [0,1,2,3,4,5])
    get_kids_obligation = Obligation("Get kids", 
                                start_time= time(14,00), 
                                end_time = time(15,00), 
                                location = None, 
                                weekdays = [0,1,2,3,4,5])
    cook_obligation = Obligation("Cook", 
                                start_time= time(16,00), 
                                end_time = time(17,00), 
                                location = kitchen, 
                                weekdays = [0,1,2,3,4,5])
    dinner_obligation = Obligation("Dinner", 
                                start_time= time(17,00), 
                                end_time = time(18,00), 
                                location = living_room, 
                                weekdays = [0,1,2,3,4,5])
    bring_to_bed_obligation = Obligation("Put Coline to bed", 
                                start_time= time(19,30), 
                                end_time = time(20,00), 
                                location = bedroom2, 
                                weekdays = [0,1,2,3,4,5])
    school_obligation = Obligation("School", 
                                start_time= time(7,00), 
                                end_time = time(15,00), 
                                location = None, 
                                weekdays = [0,1,2,3,4,5])
    
    parent1.add_obligation(work_parent_1_obligation)
    parent1.add_obligation(get_kids_obligation)
    parent1.add_obligation(cook_obligation)
    parent1.add_obligation(dinner_obligation)

    parent2.add_obligation(work_parent_2_obligation)
    parent2.add_obligation(dinner_obligation)
    parent2.add_obligation(bring_to_bed_obligation)

    child1.add_obligation(school_obligation)
    child1.add_obligation(dinner_obligation)
    child1.add_obligation(bring_to_bed_obligation)

    child2.add_obligation(school_obligation)
    child2.add_obligation(dinner_obligation)


    # create changes
    child_2_move_out = Move_Out_Change(datetime(year = 2021, month = 6, day = 2, hour = 0, minute = 0), child2)
    child_2_move_in = Move_In_Change(datetime(year = 2021, month = 9, day = 2, hour = 0, minute = 0), child2)
    scenario.changes.append(child_2_move_out)
    scenario.changes.append(child_2_move_in)

    remove_cooking_change = Obligation_Remove_Change(datetime(year = 2021, month = 3, day = 2, hour = 0, minute = 0), parent1, "Cook")
    add_cooking_change = Obligation_Remove_Change(datetime(year = 2021, month = 4, day = 2, hour = 0, minute = 0), parent1, "Cook")
    scenario.changes.append(remove_cooking_change)

    return scenario

