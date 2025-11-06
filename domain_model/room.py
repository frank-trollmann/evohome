

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


    def __init__(self, name, x, y, functions = []):
        """
            Constructor.

            Args:
                name (string): the name of the room.
                x (int): the x coordinate of the room in the user interface.
                y (int): the y coordinate of the room in the user interface.
                functions (string[]): the functions of the room. See ROOM_FUNCTION_* constants.
        """
        self.name = name
        self.x = x
        self.y = y
        self.functions = []
        self.functions.extend(functions)
        self.persons = []
        