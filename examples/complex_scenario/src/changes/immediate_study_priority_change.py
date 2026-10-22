

from copy import copy
from domain_model.changes.scheduled_change import Scheduled_Change


class Immediate_Study_Priority_Change(Scheduled_Change):
    """
        This class represents a custom implementation of a gradual change that shifts the sleep times of a person
        by shifting the start and end time of their breakfast and dinner obligation.
 
    """
    def __init__(self, datetime, campus, delta):
        """
            Constructor.

            Args:
                datetime (datetime): the date and time when the change should start.
                duration (int): the number of days this change should happen over.
                delta(float): priority change
                campus (Campus): the campus.

        """
        super().__init__(datetime)
        self.delta = delta
        self.campus = campus



    def execute(self, _):
        """
            sets the new value
        """
        for student in self.campus.students:
            study_outside_activity_priority = student.get_leisure_activity_priority("Study Outside")
            student.change_leisure_activity_priority("Study Outside", study_outside_activity_priority + self.delta)
            
            study_library_activity_priority =  student.get_leisure_activity_priority("Study Library")
            student.change_leisure_activity_priority("Study Library", study_library_activity_priority + self.delta)

            study_dorm_activity_priority = student.get_leisure_activity_priority("Study in Dorm")
            student.change_leisure_activity_priority("Study in Dorm", study_dorm_activity_priority + self.delta)


            
