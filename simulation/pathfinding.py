
from collections import deque
from copy import copy
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

    def reset_path_cache(self):
        """
            Reset path cache.
            This should only be done if the paths may change.
        """
        self.paths.clear()

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
        if not self.has_path(start_room, end_room):
            self.__calculate_paths(house, start_room, [end_room])
        
        if(self.has_path(start_room,end_room)):
            return self.paths[start_room.name][end_room.name]
        else:
            return None


    def get_closest_room(self,house, start_room, end_rooms):
        if start_room is None:
            start_room = house.get_exit()

        unknown_end_rooms = [room for room in end_rooms if not self.has_path(start_room, room)]
        self.__calculate_paths(house,start_room, unknown_end_rooms)

        possible_paths = [self.__retrieve_path_from_cache(start_room, end_room) for end_room in end_rooms]
        possible_paths = [path for path in possible_paths if path is not None]

        closest_path = min(possible_paths,key= lambda path: len(path))

        # special case: path is empty if we are already at the goal.
        if(len(closest_path) is 0):
            return start_room
        else:
            return closest_path[-1]


    def __retrieve_path_from_cache(self,start_room, end_room):
        """
            retrieves a path from cache.
        """
        return self.paths.get(start_room.name,{}).get(end_room.name,None)

    def __calculate_paths(self, house, start_room, end_rooms):
        """
            Calculates paths to a set of end rooms.
            Paths are stored via add_path and can be retrieved from cache afterwards.
        """
        remaining_end_rooms = [] + end_rooms

        open_list = deque([(start_room,[])])
        closed_list = []

        while len(open_list) > 0 and len(remaining_end_rooms) > 0:
            current_room, path = open_list.popleft()
            closed_list.append(current_room)
            if current_room in remaining_end_rooms:
                self.add_path(start_room, current_room, path)
                remaining_end_rooms.remove(current_room)

            adjacent_rooms = house.get_adjacent_rooms(current_room)
            for adjacent_room in adjacent_rooms:
                if(adjacent_room not in closed_list):
                    open_list.append((adjacent_room, path + [adjacent_room]))