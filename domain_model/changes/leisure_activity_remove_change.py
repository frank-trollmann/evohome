
from domain_model.changes.scheduled_change import Scheduled_Change


class Leisure_Activity_Remove_Change(Scheduled_Change):
    """
        This class represents a change where a person gives up a leisure activity
    """
    def __init__(self, datetime, person, activity_name):
        """
            Constructor.

            Args:
                datetime (datetime): the date and time when the change should be executed.
                person (Person): the person who moves in.
                activity_name (Obligation): the name of the activity.
        """
        super().__init__(datetime)
        self.person = person
        self.activity_name = activity_name
    
    def execute(self, _):
        """
            Removes the person from the simulation.
        """
        self.person.remove_leisure_activity(self.activity_name)
        