

class Gradual_Change:
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
        self.duration = duration
        self.current_day = 0

    def execute(self, simulation):
        """
            Executes the start of the change.

            Args:
                simulation (Scenario_Simulator): the simulation.
        """
        self.current_day = 0
        self.execute_gradual_change()
        simulation.add_gradual_change(self)

    def on_next_day(self, simulation):
        """
            called to notify the gradual change of a new day.
            Args:
                simulation (Scenario_Simulator): the simulation.
        """
        self.current_day+= 1
        self.execute_gradual_change()
        if self.current_day >= self.duration:
            simulation.remove_gradual_change(self)

    def execute_gradual(self):
        """
            Executes a 

            Args:
                simulation (Simulation): the simulation.
        """
        pass

