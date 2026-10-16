

from datetime import time

from examples.complex_scenario.src.school.campus_random_generator import Campus_Random_Generator



def get_random_color():
    return (Campus_Random_Generator._generator.randint(0,255), Campus_Random_Generator._generator.randint(0,255), Campus_Random_Generator._generator.randint(0,255))



def get_random_time_between(start_hours, start_mins, end_hours, end_mins):
    difference_in_mins = (end_hours - start_hours)*60 + end_mins - start_mins
    random_mins = Campus_Random_Generator._generator.randint(0,difference_in_mins) + start_mins
    return time(start_hours + random_mins // 60, random_mins % 60)

