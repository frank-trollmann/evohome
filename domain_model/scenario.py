

class Scenario_Configuration:
    """
        This class represents the configuration of a scenario.
        The scenario defines the setup of the simulation. It consists of:
        - a house with rooms and transitions through which persons can move.
        - a set of persons, each with their own obligations and leisure activities.
        - a set of changes that will alter the scenario at specific points in time.
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

    def remove_person(self,person):
        """
            Removes a person from the scenario.

            Args:
                person (Person): the person to remove
        """
        self.persons.remove(person)
        person.move_to_room(None)

    def get_room_names(self):
        """
            Gets the names of all rooms in the house.
            Room names will be sorted alphabetically by name.

            Returns:
                string[]: the names of all rooms.
        """
        room_names = self.house.rooms.keys()
        return sorted(room_names)

