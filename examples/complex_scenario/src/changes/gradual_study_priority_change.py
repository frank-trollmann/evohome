
from copy import copy

from domain_model.changes.gradual_changes.gradual_change import Gradual_Change


class Gradual_Study_Priority_Change(Gradual_Change):
    """
        This class represents a custom implementation of a gradual change that shifts the sleep times of a person
        by shifting the start and end time of their breakfast and dinner obligation.
 
    """
    def __init__(self, datetime, duration, campus, day_delta):
        """
            Constructor.

            Args:
                datetime (datetime): the date and time when the change should start.
                duration (int): the number of days this change should happen over.
                day_delta(float): priority change per day.
                campus (Campus): the campus.

        """
        super().__init__(datetime,duration)
        self.day_delta = day_delta
        self.campus = campus



    def execute_gradual_change(self):
        """
            Ran on every gradual change.
            Needs to be overwritten for custo implementations of Gradual_Change
        """
        for student in self.campus.students:
            study_outside_activity_priority = student.get_leisure_activity_priority("Study Outside")
            student.change_leisure_activity_priority("Study Outside", study_outside_activity_priority + self.day_delta)
            
            study_library_activity_priority =  student.get_leisure_activity_priority("Study Library")
            student.change_leisure_activity_priority("Study Library", study_library_activity_priority + self.day_delta)

            study_dorm_activity_priority = student.get_leisure_activity_priority("Study in Dorm")
            student.change_leisure_activity_priority("Study in Dorm", study_dorm_activity_priority + self.day_delta)


            
