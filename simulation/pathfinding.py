
from collections import deque
from sys import path


class Pathfinding:
    """
        Class for helping with pathfinding from room to room.
        This class applies breadth first search to find paths and dynamic programming to avoid recalculating paths.
        Accessed via Singleton pattern.
    """
    _instance = None

    def __init__(self):
        raise RuntimeError('Trying to call constructor of Singleton. Call instance() instead')

    @classmethod
    def instance(cls): 
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.paths = {}
        return cls._instance

    def add_path(self,start_room, end_room, path):
        paths_from_start = self.paths.get(start_room.name, None)
        if paths_from_start is None:
            paths_from_start = {}
            self.paths[start_room.name] = paths_from_start

        paths_from_start[end_room.name] = path

    def has_path(self, start_room, end_room):
        paths_from_start = self.paths.get(start_room.name, None)
        if paths_from_start is None:
            return False
        return end_room.name in paths_from_start
    
    
    def get_path(self, house, start_room, end_room):
        if self.has_path(start_room, end_room):
            return self.paths[start_room][end_room]
        
        path = self.__calculate_path(house, start_room, end_room)
        self.add_path(start_room, end_room, path)
        return path
    
    def __calculate_path(self, house, start_room, end_room):

        open_list = deque([(start_room,[])])
        closed_list = []

        while len(open_list) > 0:
            current_room, path = open_list.popleft()
            closed_list.append(current_room)
            if current_room == end_room:
                return path

            adjacent_rooms = house.get_adjacent_rooms(current_room)
            for adjacent_room in adjacent_rooms:
                if(adjacent_room not in closed_list):
                    open_list.append((adjacent_room, path + [adjacent_room]))

        return None