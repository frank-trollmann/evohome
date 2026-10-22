

import math

from domain_model.changes.scheduled_change import Scheduled_Change


class Gradual_Change (Scheduled_Change):
    """
        This class represents a gradual change that starts on a specific day and stretches over a number of days.
        This is the superclass for all these changes.
    """
    def __init__(self, datetime, duration):
        """
            Constructor.

            Args:
                datetime (datetime): the date and time when the change should start.
                duration (int): the number of days this change should happen over.

        """
        self.datetime = datetime
        self.duration_in_days = duration
        self.current_day = 0

    def execute(self, simulation):
        """
            Executes the start of the change.

            Do not overwrite this, unless you know what you are doing. If you need to hook into the start of the execution, use on_execution_start.

            Args:
                simulation (Scenario_Simulator): the simulation.
        """
        self.current_day = 0
        self._on_execution_start(simulation)
        self._on_execute_gradual_change()
        simulation.add_gradual_change(self)

    def on_next_day(self, simulation):
        """
            Called to notify the gradual change of a new day.

            Args:
                simulation (Scenario_Simulator): the simulation.
        """
        self.current_day+= 1
        self._on_execute_gradual_change()
        if self.current_day >= self.duration_in_days:
            simulation.remove_gradual_change(self)


    def get_progress_fraction(self):
        """
            Gets the current progress of the change. 

            Returns: the progress as a float between 0(begin of change) and 1 (end of change).
        """
        fraction = float(self.current_day) / self.duration_in_days
        return max(0.0,min(1.0,fraction))

    def _on_execution_start(self, simulation):
        """
            Called to react to begin of change.
            Interface for custom implementation.

            Args:
                            simulation (Scenario_Simulator): the simulation.
        """
        pass

    def _on_execute_gradual_change(self):
        """
            Called to implement the gradual change. 
            Interface for custom implementation.
        """
        pass

