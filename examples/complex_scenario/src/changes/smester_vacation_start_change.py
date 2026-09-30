from domain_model.changes.scheduled_change import Scheduled_Change


class Semester_Vacation_Start_Change(Scheduled_Change):
    """
        This class represents a change where a semester vacation starts.
    """
    def __init__(self, datetime, campus):
        """
            Constructor.

            Args:
                datetime (datetime): the date and time when the change should be executed.
                campus (Campus): the campus affected by the change.
        """
        super().__init__(datetime)
        self.campus = campus
    
    def execute(self, simulator):
        """
            sets the campus to semester vacation mode
        """

        self.campus.set_to_semester_vacation()
        