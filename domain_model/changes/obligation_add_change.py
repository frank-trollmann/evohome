
from domain_model.changes.scheduled_change import Scheduled_Change


class Obligation_Add_Change(Scheduled_Change):
    """
        This class represents a change where a person gets a new obligation
    """
    def __init__(self, datetime, person, obligation):
        """
            Constructor.

            Args:
                datetime (datetime): the date and time when the change should be executed.
                person (Person): the person who moves in.
                obligation (Obligation): the obligation to add.
        """
        super().__init__(datetime)
        self.person = person
        self.obligation = obligation
    
    def execute(self, _):
        """
            adds the obligation.
        """
        self.person.add_obligation(self.obligation)
        