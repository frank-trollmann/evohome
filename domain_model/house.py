
class House:

    def __init__(self):
        self.rooms = {}
        self.transitions = {}
        self.rooms_by_function = {}


    def add_room(self, room):
        self.rooms[room.name] = room
        self.transitions[room.name] = []
        for function in room.functions:
            self.add_room_function(function,room)
    
    def add_room_function(self,function,room):
        if self.rooms_by_function.get(function,None) == None:
            self.rooms_by_function[function] = []
        self.rooms_by_function[function].append(room.name)

    def get_rooms_by_function(self,function):
        names = self.rooms_by_function.get(function,[])
        rooms = []
        for name in names:
            rooms.append(self.rooms.get(name,None))
        return rooms

    def add_transtion(self,room1, room2):
        self.transitions[room1.name].append(room2.name)
        self.transitions[room2.name].append(room1.name)


    
        