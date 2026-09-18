
from domain_model.changes.scheduled_change import Scheduled_Change


class Work_Location_Change(Scheduled_Change):
    """
        Custom change to adjust work location of Bettina
    """
    def __init__(self, datetime, work_obligation, new_location ):
        super().__init__(datetime)
        self.work_obligation = work_obligation
        self.new_location = new_location
    
    def execute(self, _ ):
        self.work_obligation.location = self.new_location


        