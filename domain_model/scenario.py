

class Scenario_Configuration:
    """
        This class represents the configuration of a scenario.
        The scenario defines the initial setup and a set of change sto be executed at specific times.
    """

    def __init__(self):
        """
            Constructor.
            Initializes an empty scenario.
        """
        self.background_image = None
        self.house = None
        self.persons = []
        self.startTime = None
        self.changes = []

