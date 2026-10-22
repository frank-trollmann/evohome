from operator import is_
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


def create_gradual_change_scenario():
    """
        Assembles all aspects of the gradual change scenario, including the room setup, persons, schedules and changes.

        returns: The scenario (ScenarioConfiguration)
    
    """

    # create base setup of scenario and house
    scenario = Scenario_Configuration()
    scenario.background_image = "examples/gradual_change_scenario/images/house_1.png"
    house = House()
    scenario.house = house
    scenario.startTime = datetime(year = 2020, month = 1, day = 1, hour = 0, minute = 0)


    # create rooms and transitions
    bath = Room("Bath", 220, 230, functions = [Room.FUNCTION_BATHROOM])
    sleep = Room("Sleep", 530, 230,  functions = [Room.FUNCTION_SLEEP])
    living = Room("Living", 530, 540, functions = [Room.FUNCTION_OFFICE, Room.FUNCTION_LEISURE], ressources=["PC"])
    kitchen = Room("Kitchen", 220, 540, functions = [Room.FUNCTION_COOK])
    hallway = Room("Hallway", 220, 380, is_exit=True)
    
    house.add_room(bath)
    house.add_room(sleep)
    house.add_room(living)
    house.add_room(kitchen)
    house.add_room(hallway)

    house.add_transtion(sleep, living)
    house.add_transtion(living, kitchen)
    house.add_transtion(kitchen, hallway)
    house.add_transtion(living, hallway)
    house.add_transtion(hallway, bath)


    # create Obligations
    weekday_breakfast_obligation = Obligation("Breakfast", 
                                start_time= time(7,00), 
                                end_time = time(7,30), 
                                location = kitchen, 
                                weekdays = [0,1,2,3,4])
    weekday_university_obligation = Obligation("University", 
                                        start_time= time(10,00), 
                                        end_time = time(16,00), 
                                        location = None, 
                                        weekdays = [0,1,2,3,4])
    weekday_dinner_obligation = Obligation("Dinner", 
                                    start_time= time(21,00), 
                                    end_time = time(21,30), 
                                    location = kitchen, 
                                    weekdays = [0,1,2,3,4])
    weekend_breakfast_obligation = Obligation("Breakfast", 
                                    start_time= time(10,00), 
                                    end_time = time(10,30), 
                                    location = kitchen, 
                                    weekdays = [5,6])
    weekend_lunch_obligation = Obligation("Lunch", 
                                            start_time= time(14,00), 
                                            end_time = time(14,30), 
                                            location = kitchen, 
                                            weekdays = [5,6])
    weekend_dinner_obligation = Obligation("Dinner", 
                                        start_time= time(23,00), 
                                        end_time = time(23,30), 
                                        location = kitchen, 
                                        weekdays = [5,6])


    # create leisure activities
    socialize_activity = Leisure_Activity("Socializing", 
                                            location_options = None,
                                            min_duration= 30, 
                                            max_duration= 120)
    study_activity = Leisure_Activity("Studying", 
                                                location_options = [sleep],
                                                min_duration= 30, 
                                                max_duration= 90)
    snacking_activity = Leisure_Activity("Snacking", 
                                                    location_options = [kitchen],
                                                    min_duration= 10, 
                                                    max_duration= 30)
    watching_tv_activity = Leisure_Activity("Watching TV", 
                                                        location_options = [living],
                                                        min_duration= 10, 
                                                        max_duration= 180)



    # Create person.
    # give aline generous wakeup and sleep times so they can be influenced by obligations
    alina = Person("Alina", (255, 0, 0),wake_up_time= time(11,00), sleep_time = time(21,00))
    alina.sleep_room = sleep
    scenario.add_person(alina)
    alina.add_obligation(weekday_breakfast_obligation)
    alina.add_obligation(weekday_university_obligation)
    alina.add_obligation(weekday_dinner_obligation)
    alina.add_obligation(weekend_breakfast_obligation)
    alina.add_obligation(weekend_lunch_obligation)
    alina.add_obligation(weekend_dinner_obligation)
    alina.add_leisure_activity(socialize_activity,2)
    alina.add_leisure_activity(study_activity,1)
    alina.add_leisure_activity(snacking_activity,2)
    alina.add_leisure_activity(watching_tv_activity,4)

    
    # create changes March - April
    sleep_later_weekday = Gradual_Sleep_Cycle_Change(datetime= datetime(year = 2020, month = 3, day = 1, hour = 0, minute = 0),
                                                      duration =  31 + 30, # days March and April 2020
                                                      shift_in_mins = 120,
                                                      breakfast_obligation= weekday_breakfast_obligation,
                                                      dinner_obligation= weekday_dinner_obligation)
    scenario.changes.append(sleep_later_weekday)

    # create changes July - August
    sleep_earlier_weekday = Gradual_Sleep_Cycle_Change(datetime= datetime(year = 2020, month = 7, day = 7, hour = 0, minute = 0),
                                                          duration =  31 + 31, # days in July and August 2020
                                                          shift_in_mins = -120,
                                                          breakfast_obligation= weekday_breakfast_obligation,
                                                          dinner_obligation= weekday_dinner_obligation)
    scenario.changes.append(sleep_earlier_weekday)
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

    return scenario

