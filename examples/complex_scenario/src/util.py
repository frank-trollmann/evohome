

from datetime import time
from examples.complex_scenario.src.school.campus_random_generator import Campus_Random_Generator


"""
    convenience methods for the campus setup
"""


def get_random_color():
    """
        Returns a random color. 
        Used for assigning colors to students.

        Returns:
            A python tuple representing rgb values
    """
    return (Campus_Random_Generator._generator.randint(0,255), Campus_Random_Generator._generator.randint(0,255), Campus_Random_Generator._generator.randint(0,255))



def get_random_time_between(start_hours, start_mins, end_hours, end_mins):
    """
        Returns a random time between a start and end time

        params:
            start_hours (Int): the hour of the start time
            start_mins (Int): the minutes of the start time
            end_hours (Int): the hour of the end time
            end_mins (Int): the minutes of the end time

        returns: a Datetime.time object in between start and end time.
    """
    difference_in_mins = (end_hours - start_hours)*60 + end_mins - start_mins
    random_mins = Campus_Random_Generator._generator.randint(0,difference_in_mins) + start_mins
    return time(start_hours + random_mins // 60, random_mins % 60)

