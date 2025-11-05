

class Schedule_Item:
    """
        Represents a single entry in the schedule of a person.
        The item has the following properties:
        - start time: the time of intended start (datetime.time)
        - end time: the time of intended end (datetime.time)
        - activity_type: The type of activity (string, see constants in this class)
        - rooms: The list of rooms this activity can be carried out in. The list represents priorities. We assume the first entry is the actual room but if it is unusable, the next entries can be used as well.

    """
    ACTIVITY_TYPE_SLEEP = "SLEEP"
    ACTIVITY_TYPE_OBLIGATION = "OBLIGATION"
    ACTIVITY_TYPE_FREE_TIME = "FREE_TIME"

    def __init__(self, description, start_time, end_time, activity_type, rooms):
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.activity_type = activity_type
        self.rooms = rooms
    
    def get_room(self):
        """
            Get the room of this activity if one exists.
        """
        if self.rooms == None or len(self.rooms) == 0:
            return None
        return self.rooms[0]