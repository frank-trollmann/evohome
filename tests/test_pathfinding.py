import unittest

from domain_model.house import House
from domain_model.room import Room
from simulation.pathfinding import Pathfinding


class Test_Pathfinding(unittest.TestCase):
    """
        tests Pathfinding
    """

    def setUp(self):
        # set up mock house
        self.house = House()
        self.room_1 = Room("Room_1", 0, 0)
        self.room_2 = Room("Room_2", 0, 0)
        self.room_3 = Room("Room_3", 0, 0)
        self.room_4 = Room("Room_4", 0, 0)
        self.room_5 = Room("Room_5", 0, 0)

        self.house.add_room(self.room_1)
        self.house.add_room(self.room_2)
        self.house.add_room(self.room_3)
        self.house.add_room(self.room_4)
        self.house.add_room(self.room_5)

        self.house.add_transtion(self.room_1,self.room_2)
        self.house.add_transtion(self.room_1,self.room_3)
        self.house.add_transtion(self.room_2,self.room_3)
        self.house.add_transtion(self.room_3,self.room_4)
 

    def test_find_path(self):
       pathfinding = Pathfinding.instance()
       
       assert not pathfinding.has_path(self.room_1,self.room_4), "Path exists before calculation."
       
       path = pathfinding.get_path(self.house, self.room_1, self.room_4)
       assert len(path)  == 2, f"Path length wrong. Length is {len(path)}"

       assert pathfinding.has_path(self.room_1,self.room_4), "Path does not exist after calculation."
   
    def test_find_path_impossible(self):
       pathfinding = Pathfinding.instance()

       path = pathfinding.get_path(self.house, self.room_1, self.room_5)
       assert path is None, f"Found a path where none should exist."


    def tearDown(self):
        Pathfinding.__instance = None
