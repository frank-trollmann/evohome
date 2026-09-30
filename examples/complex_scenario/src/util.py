
import random
from datetime import time


def get_random_color():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))



def get_random_time_between(start_hours, start_mins, end_hours, end_mins):
    difference_in_mins = (end_hours - start_hours)*60 + end_mins - start_mins
    random_mins = random.randint(0,difference_in_mins) + start_mins
    return time(start_hours + random_mins // 60, random_mins % 60)

