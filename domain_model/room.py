

class Room:

    FUNCTION_SLEEP = "Sleeping"
    FUNCTION_BATHROOM = "Bathroom"
    FUNCTION_LEISURE = "Leisure"
    FUNCTION_COOK = "Cooking"
    FUNCTION_EAT = "Eating"
    FUNCTION_OFFICE = "Working"


    def __init__(self, name, x, y, functions = []):
        self.name = name
        self.x = x
        self.y = y
        self.functions = []
        self.functions.extend(functions)
        self.persons = []
        