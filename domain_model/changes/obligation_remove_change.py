
from domain_model.changes.scheduled_change import Scheduled_Change


class Obligation_Remove_Change(Scheduled_Change):
    """
        This class represents a change where a person looses an obligation
    """
    def __init__(self, datetime, person, obligation_name):
        """
            Constructor.

            Args:
                datetime (datetime): the date and time when the change should be executed.
                person (Person): the person who moves in.
                obligation (Obligation): the obligation to add.
        """
        super().__init__(datetime)
        self.person = person
        self.obligation_name = obligation_name
    
    def execute(self, _):
        """
            Removes the person from the simulation.
        """
        self.person.remove_obligation(self.obligation_name)
        