

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
    
    def add_person(self, person):
        """
            Adds a person to the scenario and moves them to their sleep room.

            Args:
                person (Person): the person to add.
        """
        self.persons.append(person)
        person.move_to_room(person.sleep_room)

    def get_room_names(self):
        """
            Gets the names of all rooms in the house.
            Room names will be sorted by first name

            Returns:
                string[]: the names of all rooms.
        """
        room_names = self.house.rooms.keys()
        return sorted(room_names)

