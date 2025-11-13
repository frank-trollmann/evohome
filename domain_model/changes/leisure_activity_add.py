
from domain_model.changes.scheduled_change import Scheduled_Change


class Leisure_Activity_Add_Change(Scheduled_Change):
    """
        This class represents a change where a person adds a new activity for their leisure time.
    """
    def __init__(self, datetime, person, activity, priority):
        """
            Constructor.

            Args:
                datetime (datetime): the date and time when the change should be executed.
                person (Person): the person who moves in.
                activity (LeisureActivity): the activity to add.
                priority (int): the priority of the activity.
        """
        super().__init__(datetime)
        self.person = person
        self.activity = activity
        self.priority = priority
    
    def execute(self, _):
        """
            adds the activity
        """
        self.person.add_leisure_activity(self.activity, self.priority)
        