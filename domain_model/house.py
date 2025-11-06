
class House:
    """
        This class represents the simulated house.
        The house is represented as a graph of rooms, where edges represent connections between rooms.
        This graph will be used for simulating movement in the house. 
    """

    def __init__(self):
        self.rooms = {}
        self.transitions = {}
        self.rooms_by_function = {}


    def add_room(self, room):
        """
            Adds a room to the house and registers it's functions

            Args:
                room (Room): the room to add.
        """
        self.rooms[room.name] = room
        self.transitions[room.name] = []
        for function in room.functions:
            self.__add_room_function(function,room)
    

    def get_rooms_by_function(self,function):
        """
            Retrieves all rooms of a certain function.

            Args: 
                function (string): the function
            
            Returns:
                Rooms[]: all rooms that have this function.
        """
        names = self.rooms_by_function.get(function,[])
        rooms = []
        for name in names:
            rooms.append(self.rooms.get(name,None))
        return rooms

    def add_transtion(self,room1, room2):
        """
            Adds a bidirectional transition between two rooms. 
            The rooms are not added and need to be added separately using add_room

            Args:
                room1 (Room): the source room.
                room2 (Room): the target room.
        """
        self.transitions[room1.name].append(room2.name)
        self.transitions[room2.name].append(room1.name)


    def __add_room_function(self, function, room):
        """
            Sets the function of a room. The room already needs to be added via add_room.

            Args: 
                function (string): the function
                room (Room): the room  
        """
        if self.rooms_by_function.get(function,None) == None:
            self.rooms_by_function[function] = []
        self.rooms_by_function[function].append(room.name)
        