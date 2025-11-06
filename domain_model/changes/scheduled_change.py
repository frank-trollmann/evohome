

class Scheduled_Change:
    """
        This class represents a change that is scheduled to happen at a specific date and time.
        This is the superclass for all possible changes.
    """
    def __init__(self, datetime):
        """
            Constructor.

            Args:
                datetime (datetime): the date and time when the change should be executed.
        """
        self.datetime = datetime

    def execute(self, simulation):
        """
            Executes the change by modifying the given simulation.

            Args:
                simulation (Simulation): the simulation.
        """
        pass
