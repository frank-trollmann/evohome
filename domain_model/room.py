

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


    def __init__(self, name, x, y, is_outside = False, functions = [], ressources = [], is_exit = False, weekdays = None, opening_time = None, closing_time = None):
        """
            Constructor.

            Args:
                name (string): the name of the room.
                x (int): the x coordinate of the room in the user interface.
                y (int): the y coordinate of the room in the user interface.
                functions (string[]): the functions of the room. See ROOM_FUNCTION_* constants.
                ressources (string[]): the ressources available in this room (e.g., furniture).
                is_exit (bool): True if the room is an exit from the house.
                weekdays (int[]): The weekdays during which the room is open. None is interpreted as being open every day.
                opening_time (time): the time the room opens. None is interpreted as being open around the clock.
                closing_time (time): the time the room closes. None is interpreted as being open around the clock.
        """
        self.name = name
        self.x = x
        self.y = y
        self.functions = [] + functions
        self.free_ressources = set(ressources)
        self.blocked_ressources = set()
        self.persons = []
        self.is_outside = is_outside
        self.is_exit = is_exit
        self.is_active = True
        self.weekdays = weekdays
        self.opening_time = opening_time
        self.closing_time = closing_time

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

    def set_active(self, active):
        """
            sets the room to be active or inactive.
            Inactive rooms are treated as being not part of the house. They are ignored in pathfinding and activities.
        """
        self.is_active = active

    def is_available(self, datetime):
        """
            Returns whether or not the room is available to be used for a specific time.

            Args:
                datetime (datetime): the desired date and time for availability.
        """
        if not self.is_active:
            return False

        weekday = datetime.weekday()
        if self.weekdays != None and weekday not in self.weekdays:
            return False

        time = datetime.time()
        if(self.opening_time != None and self.closing_time != None):
            return time > self.opening_time and time < self.closing_time

        return True
        

    def add_ressources(self, ressource_list):
        """
            Adds ressources to the room.
            Initially, these ressources will be free.

            Args:
                ressources (list<string>): the ressources to add.
        """
        self.free_ressources.update(ressource_list)

    def remove_ressources(self,ressource_list):
        """
            Removes ressources from the room.
            
            Args:
                ressources (list<string>): the ressources to remove.
        """
        removed_ressources = set(ressource_list)
        self.free_ressources -= removed_ressources
        self.blocked_ressources -= removed_ressources
        