
import random


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
        self.exits = []


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

        if(room.is_exit):
            self.exits.append(room)
    

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

    def add_transtion(self, room1, room2):
        """
            Adds a bidirectional transition between two rooms.
            The two rooms need to be already part of the house.

            Args:
                room1 (Room): the source room.
                room2 (Room): the target room.
        """
        if not room1.name in self.rooms.keys():
            raise Exception(f"Trying to add transition while {room1.name} is not part of house.")
        if not room2.name in self.rooms.keys():
            raise Exception(f"Trying to add transition while {room2.name} is not part of house.")
        
        self.transitions[room1.name].append(room2)
        self.transitions[room2.name].append(room1)

    def get_adjacent_rooms(self, room):
        """
            returns the rooms adjacent to a given room
        """
        return [neighbor for neighbor in self.transitions[room.name] if neighbor.is_active]

    def get_exit(self):
        """
            Finds a random exit from the house.
            Returns the Room that contains the exit or None if there isn't one.
        """
        exits = [room for room in self.exits if room.is_active]
        if len(exits) == 0:
            return None
        else:
            return random.choice(exits)



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
        