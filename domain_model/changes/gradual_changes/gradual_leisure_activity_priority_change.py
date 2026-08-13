

from domain_model.changes.gradual_changes.gradual_change import Gradual_Change


class Gradual_Leisure_Activity_Priority_Change(Gradual_Change):
    """
        This class represents a gradual change that starts on a specific day and stretches over a number of days.
        This is the superclass for all these changes.
    """
    def __init__(self, datetime, duration, person, activity_name, start_priority, end_priority):
        """
            Constructor.

            Args:
                datetime (datetime): the date and time when the change should start.
                duration (int): the number of days this change should happen over.

        """
        super().__init__(datetime,duration)
        self.person = person
        self.activity_name = activity_name;
        self.start_priority = start_priority;
        self.end_priority = end_priority;

    def execute_gradual(self,_):
        priority = self.start_priority + self.get_progress_fraction()* (self.end_priority - self.start_priority)
        self.person.change_leisure_activity_priority(self.activity_name, priority)


