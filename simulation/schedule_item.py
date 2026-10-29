

class Schedule_Item:
    """
        Represents a single entry in the schedule of a person.
    """
    ACTIVITY_TYPE_SLEEP = "SLEEP"
    ACTIVITY_TYPE_OBLIGATION = "OBLIGATION"
    ACTIVITY_TYPE_FREE_TIME = "FREE_TIME"

    def __init__(self, description, start_time, end_time, activity_type, rooms):
        """
            Constructor.

            Args:
                description (string): the description of the schedule item
                start_time: (datetime.time): the time of intended start 
                end_time(datetime.time): the time of intended end
                activity_type (string): The type of activity (see constants in this class)
                rooms (list<Room>): activity_type: The type of activity (string, see constants in this class)
        """
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.activity_type = activity_type
        self.rooms = rooms
    
    def get_room(self):
        """
            Get the room of this activity if one exists.

            Returns:
                Room: the room
        """
        if self.rooms == None or len(self.rooms) == 0:
            return None
        return self.rooms[0]