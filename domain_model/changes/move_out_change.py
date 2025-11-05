
from domain_model.changes.scheduled_change import Scheduled_Change


class Move_Out_Change(Scheduled_Change):
    def __init__(self, datetime, person):
        super().__init__(datetime)
        self.person = person
    
    def execute(self, simulation):
        simulation.remove_person(self.person)
        