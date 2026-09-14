from operator import is_
from turtle import home

from tornado.autoreload import watch
from domain_model.changes.gradual_changes.gradual_leisure_activity_priority_change import Gradual_Leisure_Activity_Priority_Change
from domain_model.leisure_activity import Leisure_Activity
from domain_model.obligation import Obligation
from domain_model.scenario import Scenario_Configuration
from domain_model.house import House
from domain_model.room import Room
from domain_model.person import Person

from datetime import datetime
from datetime import time

from examples.gradual_change_scenario.src.gradual_sleep_cycle_change import Gradual_Sleep_Cycle_Change


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


    
    return scenario
    
    # create changes March - April
    sleep_later_weekday = Gradual_Sleep_Cycle_Change(datetime= datetime(year = 2020, month = 3, day = 1, hour = 0, minute = 0),
                                                      duration =  31 + 30, # days March and April 2020
                                                      shift_in_mins = 120,
                                                      breakfast_obligation= weekday_breakfast_obligation,
                                                      dinner_obligation= weekday_dinner_obligation)
    scenario.changes.append(sleep_later_weekday)
    sleep_later_weekend = Gradual_Sleep_Cycle_Change(datetime= datetime(year = 2020, month = 3, day = 1, hour = 0, minute = 0),
                                                          duration =  31 + 30, # days in feb and march 2020
                                                          shift_in_mins = 120,
                                                          breakfast_obligation= weekend_breakfast_obligation,
                                                          dinner_obligation= weekend_dinner_obligation)
    # scenario.changes.append(sleep_later_weekend)



    # create changes July - August
    sleep_earlier_weekday = Gradual_Sleep_Cycle_Change(datetime= datetime(year = 2020, month = 7, day = 7, hour = 0, minute = 0),
                                                          duration =  31 + 31, # days in July and August 2020
                                                          shift_in_mins = -120,
                                                          breakfast_obligation= weekday_breakfast_obligation,
                                                          dinner_obligation= weekday_dinner_obligation)
    scenario.changes.append(sleep_earlier_weekday)
    
    sleep_earlier_weekend = Gradual_Sleep_Cycle_Change(datetime= datetime(year = 2020, month = 7, day = 7, hour = 0, minute = 0),
                                                              duration =  31 + 31, # days in July and August 2020
                                                              shift_in_mins = -120,
                                                              breakfast_obligation= weekend_breakfast_obligation,
                                                              dinner_obligation= weekend_dinner_obligation)
    scenario.changes.append(sleep_earlier_weekend)

    prioritize_study = Gradual_Leisure_Activity_Priority_Change(datetime= datetime(year = 2020, month = 7, day = 1, hour = 0, minute = 0),
                                                              duration =  31 + 31, # days in July and August 2020
                                                              person = alina,
                                                              activity_name = study_activity.name,
                                                              start_priority = 1,
                                                              end_priority = 5)
    scenario.changes.append(prioritize_study)

    de_prioritize_tv = Gradual_Leisure_Activity_Priority_Change(datetime= datetime(year = 2020, month = 7, day = 1, hour = 0, minute = 0),
                                                                  duration =  31 + 31, # days in July and August 2020
                                                                  person = alina,
                                                                  activity_name = watching_tv_activity.name,
                                                                  start_priority = 4,
                                                                  end_priority = 1)
    scenario.changes.append(de_prioritize_tv)

    """
    
    
     # create persons
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
                                location = kitchen)
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
    """
    return scenario

