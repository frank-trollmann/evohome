

from copy import copy
import datetime

from domain_model.changes.gradual_changes.gradual_change import Gradual_Change


class Gradual_Sleep_Cycle_Change(Gradual_Change):
    """
        This class represents a custom implementation of a gradual change that shifts the sleep times of a person
        by shifting the start and end time of their breakfast and dinner obligation.
 
    """
    def __init__(self, datetime, duration, shift_in_mins, breakfast_obligation, dinner_obligation):
        """
            Constructor.

            Args:
                datetime (datetime): the date and time when the change should start.
                duration (int): the number of days this change should happen over.
                shift_in_hours(int): by how many hours the time will shift.
                breakfast_obligation (Obligation): the obligation representing breakfast.
                dinner_obligation (Obligation): the obligation representing dinner.

        """
        super().__init__(datetime,duration)
        self.shift_in_mins = shift_in_mins;
        self.breakfast_obligation = breakfast_obligation;
        self.dinner_obligation = dinner_obligation;

    def execute(self, simulation):
        """
            Executes the start of the change.
            This is overwritten to be able to preserve the initial start and end times of activities to have them available for calculations during execute_gradual.

            Args:
                simulation (Scenario_Simulator): the simulation.
        """
        self.breakfast_start = copy(self.breakfast_obligation.start_time)
        self.breakfast_end = copy(self.breakfast_obligation.end_time)
        self.dinner_start = copy(self.dinner_obligation.start_time)
        self.dinner_end = copy(self.dinner_obligation.end_time)
        super().execute(simulation)


    def execute_gradual_change(self):
        """
            Ran on every gradual change.
            Needs to be overwritten for custo implementations of Gradual_Change
        """
        progress_fraction = self.get_progress_fraction()
        current_shift_in_mins = int(progress_fraction * self.shift_in_mins)
        timedelta = datetime.timedelta(minutes=current_shift_in_mins)

        self.breakfast_obligation.start_time = self.__add_time(self.breakfast_start, timedelta)
        self.breakfast_obligation.end_time = self.__add_time(self.breakfast_end, timedelta)
        self.dinner_obligation.start_time = self.__add_time(self.dinner_start, timedelta)
        self.dinner_obligation.end_time = self.__add_time(self.dinner_end, timedelta)


    def __add_time(self, time, timedelta):
        """
            Convenience method to add time to a time object.
            Requires temporary conversion to full datetime.
        """
        fulldate = datetime.datetime(10, 1, 1, time.hour, time.minute, time.second)
        fulldate = fulldate + timedelta
        return fulldate.time()

