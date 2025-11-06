
from domain_model.changes.scheduled_change import Scheduled_Change


class Move_Out_Change(Scheduled_Change):
    """
        This class represents a change where a person moves out of the house.
    """
    def __init__(self, datetime, person):
        """
            Constructor.

            Args:
                datetime (datetime): the date and time when the change should be executed.
                person (Person): the person who moves out.
        """
        super().__init__(datetime)
        self.person = person
    
    def execute(self, simulation):
        """
            Removes the person from the simulation.
        """
        simulation.remove_person(self.person)
        