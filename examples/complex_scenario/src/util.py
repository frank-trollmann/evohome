
from simulation.random_generator import Simulation_Random_Generator

from datetime import time


def get_random_color():
    return (Simulation_Random_Generator._generator.randint(0,255), Simulation_Random_Generator._generator.randint(0,255), Simulation_Random_Generator._generator.randint(0,255))



def get_random_time_between(start_hours, start_mins, end_hours, end_mins):
    difference_in_mins = (end_hours - start_hours)*60 + end_mins - start_mins
    random_mins = Simulation_Random_Generator._generator.randint(0,difference_in_mins) + start_mins
    return time(start_hours + random_mins // 60, random_mins % 60)

