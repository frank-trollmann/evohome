from domain_model.changes.scheduled_change import Scheduled_Change
from simulation.pathfinding import Pathfinding


class Open_Dorm_B_Change(Scheduled_Change):
    """
        This class represents a change where dorm B is opened
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
            sets the dorm to open and updates the simulation visualization
        """
        self.campus.set_dorm_b_active(True)
        simulator.notify_visualization_refresh_needed() # need to redraw newly active rooms.
        Pathfinding.instance().reset_path_cache() # reset path cache because new paths may have been added.