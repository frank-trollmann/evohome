

class Room:
    """
        This class represents a room in the house.
    """

    FUNCTION_SLEEP = "Sleeping"
    FUNCTION_BATHROOM = "Bathroom"
    FUNCTION_LEISURE = "Leisure"
    FUNCTION_COOK = "Cooking"
    FUNCTION_EAT = "Eating"
    FUNCTION_OFFICE = "Working"


    def __init__(self, name, x, y, is_outside = False, functions = [], ressources = []):
        """
            Constructor.

            Args:
                name (string): the name of the room.
                x (int): the x coordinate of the room in the user interface.
                y (int): the y coordinate of the room in the user interface.
                functions (string[]): the functions of the room. See ROOM_FUNCTION_* constants.
                ressources (string[]): the ressources available in this room (e.g., furniture).
        """
        self.name = name
        self.x = x
        self.y = y
        self.functions = [] + functions
        self.free_ressources = set(ressources)
        self.blocked_ressources = set()
        self.persons = []
        self.is_outside = is_outside

    def ressources_available(self, ressources):
        """
            Checks whether the given ressources are available in this room.

            Args:
                ressources (set(string)): the ressources to check.
        """
        return ressources <= self.free_ressources
    
    def block_ressources(self,ressources):
        """
            Blocks the given ressources in this room.

            Args:
                ressources (set(string)): the ressources to block.
        """
        self.free_ressources -= ressources
        self.blocked_ressources |= ressources

    def release_ressources(self,ressources):
        """
            Releases the given ressources in this room.

            Args:
                ressources (set(string)): the ressources to release.
        """
        self.blocked_ressources -= ressources
        self.free_ressources |= ressources
        