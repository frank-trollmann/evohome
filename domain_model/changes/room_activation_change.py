
from domain_model.changes.scheduled_change import Scheduled_Change


class Room_Activation_Change(Scheduled_Change):
    """
        This class represents a change where a room becomes active or inactive at a point in time.
    """
    def __init__(self, datetime, room, active):
        """
            Constructor.

            Args:
                datetime (datetime): the date and time when the change should be executed.
                room (Room): the room to activate / deactivate
                active (Active): whether or not the room should be switched to active
        """
        super().__init__(datetime)
        self.room = room
        self.active = active
    
    def execute(self, simulator):
        """
            Args:
                simulator (ScenarioSimulator): a reference to the simulator of this scenario.
            Sets the room to be active / inactive. Also refreshes drawing background.
        """
        self.room.XXX (TODO: Needs implementation.)

        