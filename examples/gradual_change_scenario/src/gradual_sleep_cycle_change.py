

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
                shift_in_mins(int): by how many minutes the time will shift.
                breakfast_obligation (Obligation): the obligation representing breakfast.
                dinner_obligation (Obligation): the obligation representing dinner.

        """
        super().__init__(datetime,duration)
        self.shift_in_mins = shift_in_mins;
        self.breakfast_obligation = breakfast_obligation;
        self.dinner_obligation = dinner_obligation;

    def _on_execution_start(self, simulation):
        """
            Called to react to begin of change.
            Interface for custom implementation.

            Here, we preserve the initial start and end time of the activity to preserve them for calculations.

            Args:
                simulation (Scenario_Simulator): the simulation.
        """
        self.breakfast_start = copy(self.breakfast_obligation.start_time)
        self.breakfast_end = copy(self.breakfast_obligation.end_time)
        self.dinner_start = copy(self.dinner_obligation.start_time)
        self.dinner_end = copy(self.dinner_obligation.end_time)


    def _on_execute_gradual_change(self):
        """
            Called to implement the gradual change. 
            Interface for custom implementation.

            This method runs once every day and can rely on get_progress_fraction to give the right fraction.
            Here, we update the start and end times of the activities.
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

