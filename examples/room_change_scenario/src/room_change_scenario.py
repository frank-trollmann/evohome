from operator import is_
from turtle import home

from tornado.autoreload import watch
from domain_model.changes.gradual_changes.gradual_leisure_activity_priority_change import Gradual_Leisure_Activity_Priority_Change
from domain_model.changes.room_activation_change import Room_Activation_Change
from domain_model.changes.room_ressource_change import Room_Ressource_Change
from domain_model.leisure_activity import Leisure_Activity
from domain_model.obligation import Obligation
from domain_model.scenario import Scenario_Configuration
from domain_model.house import House
from domain_model.room import Room
from domain_model.person import Person

from datetime import datetime
from datetime import time

from examples.gradual_change_scenario.src.gradual_sleep_cycle_change import Gradual_Sleep_Cycle_Change
from examples.room_change_scenario.src.work_location_change import Work_Location_Change


def create_room_change_scenario():
    scenario = Scenario_Configuration()
    scenario.background_image = "examples/room_change_scenario/images/room_change_house.png"

    house = House()
    scenario.house = house
    scenario.startTime = datetime(year = 2020, month = 1, day = 1, hour = 0, minute = 0)

    # create rooms and transitions
    kitchen = Room("Kitchen", 200, 550, functions = [Room.FUNCTION_COOK])
    living_room = Room("Living Room", 250, 250,  functions = [Room.FUNCTION_LEISURE],  ressources= ["TV"])
    bedroom = Room("Bedroom", 900, 250, functions = [Room.FUNCTION_SLEEP])
    hallway_1 = Room("Hallway 1", 400, 500, is_exit= True)
    hallway_2 = Room("Hallway 2", 700, 500)
    bathroom = Room("Bathroom", 700, 650)
    hobby_room = Room("Hobby Room", 600, 250, functions = [Room.FUNCTION_LEISURE], ressources= ["Sewing Machine", "Crafting Materials", "Painting Materials"])
    home_office = Room("Home Office", 900, 550, ressources= ["PC", "DESK"])
    
    house.add_room(kitchen)
    house.add_room(living_room)
    house.add_room(hobby_room)
    house.add_room(bedroom)
    house.add_room(hallway_1)
    house.add_room(hallway_2)
    house.add_room(bathroom)
    house.add_room(home_office)

    house.add_transtion(hallway_1, hallway_2)
    house.add_transtion(hallway_1, living_room)
    house.add_transtion(living_room, kitchen)
    house.add_transtion(living_room, hobby_room)
    house.add_transtion(hallway_2, bathroom)
    house.add_transtion(hallway_2, home_office)
    house.add_transtion(hallway_2, bedroom)

    # create persons
    anna = Person("Anna", (255, 0, 0),wake_up_time= time(8,00), sleep_time = time(22,00))
    anna.sleep_room = bedroom
    scenario.add_person(anna)

    bettina = Person("Bettina", (0, 0, 255),wake_up_time= time(10,00), sleep_time = time(23,00))
    bettina.sleep_room = bedroom
    scenario.add_person(bettina)

    # create obligation schedule
    anna_weekday_breakfast_obligation = Obligation("Breakfast", 
                                start_time= time(6,00), 
                                end_time = time(6,30), 
                                location = kitchen, 
                                weekdays = [0,1,2,3,4])
    anna.add_obligation(anna_weekday_breakfast_obligation)

    anna_weekday_work_obligation = Obligation("Work", 
                                    start_time= time(8,00), 
                                    end_time = time(17,00), 
                                    location = None, 
                                    weekdays = [0,1,2,3,4])
    anna.add_obligation(anna_weekday_work_obligation)

    anna_weekend_breakfast_obligation = Obligation("Breakfast", 
                                    start_time= time(8,30), 
                                    end_time = time(9,00), 
                                    location = kitchen, 
                                    weekdays = [5,6])
    anna.add_obligation(anna_weekend_breakfast_obligation)

    anna_bettina_weekend_lunch_obligation = Obligation("Lunch", 
                                            start_time= time(13,00), 
                                            end_time = time(14,00), 
                                            location = kitchen, 
                                            weekdays = [5,6])
    anna.add_obligation(anna_bettina_weekend_lunch_obligation)
    bettina.add_obligation(anna_bettina_weekend_lunch_obligation)

    anna_bettina_dinner_obligation = Obligation("Dinner", 
                                        start_time= time(19,00), 
                                        end_time = time(20,00), 
                                        location = kitchen, 
                                        weekdays = [0,1,2,3,4,5,6])
    anna.add_obligation(anna_bettina_dinner_obligation)
    bettina.add_obligation(anna_bettina_dinner_obligation)
    
    betina_weekday_breakfast_obligation = Obligation("Breakfast", 
                                    start_time= time(9,00), 
                                    end_time = time(9,30), 
                                    location = kitchen, 
                                    weekdays = [0,1,2,3,4])
    bettina.add_obligation(betina_weekday_breakfast_obligation)
    
    bettina_weekday_work_obligation = Obligation("Work", 
                                    start_time= time(10,00), 
                                    end_time = time(18,00), 
                                    location = home_office, 
                                    weekdays = [0,1,2,3,4])
    bettina.add_obligation(bettina_weekday_work_obligation)

    bettina_weekend_breakfast_obligation = Obligation("Breakfast", 
                                        start_time= time(10,30), 
                                        end_time = time(11,00), 
                                        location = kitchen, 
                                        weekdays = [5,6])
    bettina.add_obligation(bettina_weekend_breakfast_obligation)


    # create leisure activities
    reading_activity = Leisure_Activity("Reading", 
                                location_options = [living_room, bedroom, hobby_room],
                                min_duration= 30, 
                                max_duration= 120)
    anna.add_leisure_activity(reading_activity,1)
    bettina.add_leisure_activity(reading_activity,2)

    sewing_activity = Leisure_Activity("Sewing", 
                                location_options = [living_room, bedroom, hobby_room],
                                min_duration= 60, 
                                max_duration= 90,
                                required_ressources=["Sewing Machine"])
    anna.add_leisure_activity(sewing_activity,3)

    crafting = Leisure_Activity("Crafting", 
                                location_options = [living_room, bedroom, hobby_room],
                                min_duration= 10, 
                                max_duration= 60,
                                required_ressources=["Crafting Materials"])
    anna.add_leisure_activity(crafting,4)
    bettina.add_leisure_activity(crafting,2)

    painting = Leisure_Activity("Painting", 
                                location_options = [living_room, bedroom, hobby_room],
                                min_duration= 10, 
                                max_duration= 60,
                                required_ressources=["Painting Materials"])
    anna.add_leisure_activity(painting,2)

    shopping = Leisure_Activity("Shopping", 
                                location_options = None,
                                min_duration= 60, 
                                max_duration= 120)
    anna.add_leisure_activity(shopping,2)
    bettina.add_leisure_activity(shopping,1)

    cooking = Leisure_Activity("Cooking", 
                                location_options = [kitchen],
                                min_duration= 30, 
                                max_duration= 90)
    anna.add_leisure_activity(cooking,1)

    digital_art = Leisure_Activity("Digital Art", 
                                    location_options = [home_office,living_room],
                                    min_duration= 30, 
                                    max_duration= 120,
                                    required_ressources= ["PC"])
    anna.add_leisure_activity(digital_art,1)

    self_education = Leisure_Activity("Self-Education", 
                                    location_options = [home_office,living_room, hobby_room],
                                    min_duration= 30, 
                                    max_duration= 90,
                                    required_ressources= ["PC"])
    bettina.add_leisure_activity(self_education,3)

    creative_writing = Leisure_Activity("Creative Writing", 
                                        location_options = [home_office,living_room, hobby_room],
                                        min_duration= 30, 
                                        max_duration= 90,
                                        required_ressources= ["DESK"])
    bettina.add_leisure_activity(creative_writing,3)

    gaming = Leisure_Activity("Gaming", 
                                            location_options = [home_office, living_room, hobby_room],
                                            min_duration= 10, 
                                            max_duration= 60,
                                            required_ressources= ["PC"])
    bettina.add_leisure_activity(gaming,3)

    watching_tv = Leisure_Activity("Watching TV", 
                                            location_options = [living_room],
                                            min_duration= 10, 
                                            max_duration= 60,
                                            required_ressources= ["TV"])
    anna.add_leisure_activity(watching_tv,1)
    bettina.add_leisure_activity(watching_tv,3)

    # Phase 2 changes (close home office )
    time1 = datetime(year = 2020, month = 3, day = 1, hour = 0, minute = 0)
    close_home_office_change = Room_Activation_Change(datetime= time1,
                                                          room = home_office,
                                                          active= False)
    scenario.changes.append(close_home_office_change)
    move_pc_change_1 = Room_Ressource_Change(datetime= time1,
                                           room = home_office,
                                           removed_ressources=["PC"])
    scenario.changes.append(move_pc_change_1)
    move_pc_change_2 = Room_Ressource_Change(datetime= time1,
                                               room = living_room,
                                               added_ressources=["PC"])
    scenario.changes.append(move_pc_change_2)
    work_location_change = Work_Location_Change(datetime= time1,
                                                work_obligation=bettina_weekday_work_obligation,
                                                new_location=living_room
                                                    ) 
    scenario.changes.append(work_location_change)



    # Phase 3 changes (close hobby room)
    time2 = datetime(year = 2020, month = 5, day = 1, hour = 0, minute = 0)
    close_hobby_room_change = Room_Activation_Change(datetime= time2,
                                                              room = hobby_room,
                                                              active= False)
    scenario.changes.append(close_hobby_room_change)

    move_sewing_machine_change_1 = Room_Ressource_Change(datetime= time2,
                                               room = hobby_room,
                                               removed_ressources=["Sewing Machine"])
    scenario.changes.append(move_sewing_machine_change_1)
    move_sewing_machine_change_2 = Room_Ressource_Change(datetime= time2,
                                                   room = bedroom,
                                                   added_ressources=["Sewing Machine"])
    scenario.changes.append(move_sewing_machine_change_2)



    # phase 4 changes (open home office)
    time3 = datetime(year = 2020, month = 7, day = 1, hour = 0, minute = 0)
    open_home_office_change = Room_Activation_Change(datetime= time3,
                                                          room = home_office,
                                                          active= True)
    scenario.changes.append(open_home_office_change)
    restore_pc_change_1 = Room_Ressource_Change(datetime= time3,
                                                   room = living_room,
                                                   removed_ressources=["PC"])
    scenario.changes.append(restore_pc_change_1)
    restore_pc_change_2 = Room_Ressource_Change(datetime= time3,
                                                room = home_office,
                                                added_ressources=["PC"])
    scenario.changes.append(restore_pc_change_2)
    restore_work_location_change = Work_Location_Change(datetime= time3,
                                                work_obligation=bettina_weekday_work_obligation,
                                                new_location=home_office
                                                    ) 
    scenario.changes.append(restore_work_location_change)
    move_arts_craft_change_1 = Room_Ressource_Change(datetime= time3,
                                                   room = hobby_room,
                                                   removed_ressources=["Painting Materials", "Crafting Materials"])
    scenario.changes.append(move_arts_craft_change_1)
    move_arts_craft_change_2 = Room_Ressource_Change(datetime= time3,
                                                       room = home_office,
                                                       added_ressources=["Painting Materials", "Crafting Materials"])
    scenario.changes.append(move_arts_craft_change_2)

    # phase 5 changes (open hobby room)
    time4 = datetime(year = 2020, month = 9, day = 1, hour = 0, minute = 0)
    open_hobby_room_change = Room_Activation_Change(datetime= time4,
                                                                  room = hobby_room,
                                                                  active= True)
    scenario.changes.append(open_hobby_room_change)
    restore_sewing_machine_change_1 = Room_Ressource_Change(datetime= time4,
                                                   room = bedroom,
                                                   removed_ressources=["Sewing Machine"])
    scenario.changes.append(restore_sewing_machine_change_1)
    restore_sewing_machine_change_2 = Room_Ressource_Change(datetime= time4,
                                                    room = hobby_room,
                                                    added_ressources=["Sewing Machine"])
    scenario.changes.append(restore_sewing_machine_change_2)
    restore_arts_craft_change_1 = Room_Ressource_Change(datetime= time4,
                                                   room = home_office,
                                                   removed_ressources=["Painting Materials", "Crafting Materials"])
    scenario.changes.append(restore_arts_craft_change_1)
    restore_arts_craft_change_2 = Room_Ressource_Change(datetime= time4,
                                                       room = hobby_room,
                                                       added_ressources=["Painting Materials", "Crafting Materials"])
    scenario.changes.append(restore_arts_craft_change_2)
    
    return scenario
    

