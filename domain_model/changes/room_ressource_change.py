
from domain_model.changes.scheduled_change import Scheduled_Change


class Room_Ressource_Change(Scheduled_Change):
    """
        This class represents a change where ressources get added to or removed from a room.
    """
    def __init__(self, datetime, room, added_ressources = [], removed_ressources = []):
        """
            Constructor.

            Args:
                datetime (datetime): the date and time when the change should be executed.
                room (Room): the room to change.
                added_ressources (List<String>): the ressources that will be added
                removed_ressources (List<String>): the ressources that will be removed
        """
        super().__init__(datetime)
        self.room = room
        self.added_ressources = added_ressources
        self.removed_ressources = removed_ressources
    
    def execute(self, _ ):
        """
            Args:
                simulator (ScenarioSimulator): a reference to the simulator of this scenario.
            Updates the ressources
        """
        self.room.add_ressources(self.added_ressources)
        self.room.remove_ressources(self.removed_ressources)


        